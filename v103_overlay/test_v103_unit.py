import hashlib
import os
import json
import sqlite3
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core_loader import load_core
from apple_accounts import AppleStore, install_schema
from apple_profiles import parse_proxy, proxy_identity
from apple_browser import BrowserSession, AppleFlowError
from app_updater import installed_executable
from tools.verify_native_launcher import MAGIC, FOOTER_SIZE, verify
from test_apple_workspace import event

core = load_core()


class ProxyAndMigrationTests(unittest.TestCase):
    def test_proxy_identity_is_stable_and_includes_credentials(self):
        a=parse_proxy('http://one:secret@example.test:8080')
        b=parse_proxy('http://two:secret@example.test:8080')
        self.assertEqual(proxy_identity(a),proxy_identity(dict(a)))
        self.assertNotEqual(proxy_identity(a),proxy_identity(b))
        self.assertEqual(a['server'],b['server'])

    def test_route_schema_migration_preserves_id_and_allows_same_server(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'db.sqlite';c=sqlite3.connect(p)
            c.executescript('''
            CREATE TABLE orders(id INTEGER PRIMARY KEY);
            CREATE TABLE apple_schema(version INTEGER PRIMARY KEY);
            INSERT INTO apple_schema VALUES(1);
            CREATE TABLE apple_routes(
              id TEXT PRIMARY KEY,server TEXT NOT NULL UNIQUE,state TEXT NOT NULL DEFAULT 'Not tested',
              last_check TEXT NOT NULL DEFAULT '',message TEXT NOT NULL DEFAULT '',has_auth INTEGER NOT NULL DEFAULT 0);
            INSERT INTO apple_routes VALUES('old-id','http://proxy.test:8080','Passed','when','ok',1);
            ''')
            install_schema(c)
            row=c.execute("SELECT id,server,identity,revision FROM apple_routes WHERE id='old-id'").fetchone()
            self.assertEqual(row[0],'old-id');self.assertEqual(row[1],'http://proxy.test:8080');self.assertTrue(row[2]);self.assertEqual(row[3],1)
            c.execute("INSERT INTO apple_routes(id,identity,server) VALUES('new-id','different','http://proxy.test:8080')")
            c.commit();self.assertEqual(c.execute("SELECT COUNT(*) FROM apple_routes WHERE server='http://proxy.test:8080'").fetchone()[0],2);c.close()


class UpdaterBridgeTests(unittest.TestCase):
    def test_installed_executable_prefers_persistent_launcher(self):
        with tempfile.TemporaryDirectory() as td:
            launcher=Path(td)/'AhPaTaTracker.exe';launcher.write_bytes(b'MZ')
            with patch.dict('os.environ',{'AHPATA_LAUNCHER_PATH':str(launcher)},clear=False):
                self.assertTrue(os.path.samefile(installed_executable(),launcher))

    def test_native_launcher_footer_verifies_payload(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'launcher.exe';payload=b'MZ'+b'payload-v103'*20;digest=hashlib.sha256(payload).digest()
            version=b'1.0.3'.ljust(32,b'\0')
            footer=MAGIC+struct.pack('<q',len(payload))+digest+version+struct.pack('<q',0)
            self.assertEqual(len(footer),FOOTER_SIZE)
            p.write_bytes(b'MZnative-stub'+payload+footer)
            self.assertEqual(verify(p,'1.0.3'),digest.hex())


class CacheProtectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.db=core.Database(Path(self.tmp.name)/'orders.db')
        a=self.db.add_account('mail@example.test');self.db.save_update(a,1,event());self.oid=self.db.query_orders()[0]['id']
    def tearDown(self):self.db.close();self.tmp.cleanup()

    def test_cache_rebuild_blocks_linked_apple_history(self):
        with self.db.conn:self.db.conn.execute("UPDATE orders SET association_state='associated',linked_apple_connection='c1' WHERE id=?",(self.oid,))
        with self.assertRaises(ValueError):self.db.reset_order_cache()
        self.assertIsNotNone(self.db.order_by_id(self.oid))

    def test_cache_rebuild_without_apple_history_still_works(self):
        self.assertIsNone(self.db.reset_order_cache());self.assertIsNone(self.db.order_by_id(self.oid))


class AssociationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.db=core.Database(Path(self.tmp.name)/'orders.db');self.store=AppleStore(self.db)
        a=self.db.add_account('mail@example.test');self.db.save_update(a,1,event());self.oid=self.db.query_orders()[0]['id']
        self.cid=self.store.add_connection('owner@example.test');self.store.connection_state(self.cid,'connected')
        self.session=BrowserSession.__new__(BrowserSession);self.session.connection=self.store.connection(self.cid);self.session.validated=True
    def tearDown(self):self.db.close();self.tmp.cleanup()
    def _snap(self):
        return {'url':'https://secure.store.apple.com/shop/order/guest/W1000000001/token','text':'W1000000001 Processing',
                'headings':['Processing'],'controls':[{'text':'Cancel Order'}],'password_prompt':False,'auth_prompt':False,'identities':[]}

    def test_unlinked_guest_management_controls_are_not_authenticated_order_read(self):
        jid=self.store.create_job(self.store.snapshot([self.oid],self.cid,'refresh'));task=self.store.take_next({self.cid})
        self.session._linked_in_listing=lambda n:False;self.session.task_page=lambda *a,**k:object();self.session.snapshot=lambda p:self._snap();self.session._assert_identity=lambda s:set()
        with self.assertRaises(AppleFlowError) as cm:self.session.read_order(task,self.db.order_by_id(self.oid),'https://example.test')
        self.assertEqual(cm.exception.code,'needs_association')


if __name__=='__main__':unittest.main(verbosity=2)
