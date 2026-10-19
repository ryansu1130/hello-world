"""v1.0.3 Qt regression gate. Temporary data only; no Apple or proxy network calls."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import gui_smoke as g
from PySide6.QtCore import Qt
from apple_accounts import AppleStore


class V103GUITests(unittest.TestCase):
    setUp=g.GUITests.setUp
    tearDown=g.GUITests.tearDown

    def page(self):
        p=self.window.apple_page
        self.window.show_page(self.window.PAGE_APPLE,self.window.apple_nav);g.APP.processEvents()
        return p

    def test_v103_branding_themes_and_guidance_controls(self):
        self.assertIn('v1.0.3',self.window.windowTitle())
        p=self.page();self.assertEqual([p.tabs.tabText(i) for i in range(p.tabs.count())],['Connection','Phone mappings','Jobs & results','Proxies'])
        self.assertEqual(p.save_routes_btn.text(),'Save Proxies');self.assertEqual(p.test_routes_btn.text(),'Test Selected (0)')
        for theme in ('light','dark'):
            self.window.apply_theme(theme);g.APP.processEvents();shot=self.window.grab();self.assertFalse(shot.isNull());self.assertTrue(shot.save(str(Path.cwd()/f'v103_{theme}.png')))

    def test_proxy_preview_keeps_valid_rows_when_another_row_is_invalid(self):
        p=self.page();p.tabs.setCurrentIndex(3)
        p.proxy_text.setPlainText('127.0.0.1:8080:user:pass\nTHIS IS NOT A PROXY')
        p.preview_routes();self.assertEqual(len(p.pending_routes),1);self.assertEqual(len(p.route_errors),1)
        self.assertTrue(p.save_routes());rows=[dict(r) for r in self.window.db.conn.execute('SELECT * FROM apple_routes')]
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['server'],'http://127.0.0.1:8080');self.assertIn('1 rejected',p.route_save_status.text())

    def test_same_endpoint_different_credentials_remain_distinct_and_selection_survives_sort(self):
        p=self.page();p.tabs.setCurrentIndex(3)
        p.proxy_text.setPlainText('127.0.0.1:8080:user1:pass1\n127.0.0.1:8080:user2:pass2')
        p.preview_routes();self.assertEqual(len(p.pending_routes),2);self.assertTrue(p.save_routes());self.assertEqual(p.routes_model.rowCount(),2)
        idx=p.routes_model.index(0,0);p.routes_model.setData(idx,Qt.Checked,Qt.CheckStateRole);chosen=set(p.routes_model.selected_ids)
        self.assertEqual(len(chosen),1);p.routes_model.sort(1,Qt.DescendingOrder);self.assertEqual(p.routes_model.selected_ids,chosen);self.assertEqual(p.test_routes_btn.text(),'Test Selected (1)')

    def test_unsaved_proxy_edit_disables_selected_proxy_test(self):
        p=self.page();p.tabs.setCurrentIndex(3);p.proxy_text.setPlainText('127.0.0.1:8080:user:pass');p.preview_routes();self.assertTrue(p.save_routes())
        p.routes_model.setData(p.routes_model.index(0,0),Qt.Checked,Qt.CheckStateRole);self.assertTrue(p.test_routes_btn.isEnabled())
        p.proxy_text.setPlainText('127.0.0.1:8081:other:pass');g.APP.processEvents();self.assertTrue(p.route_dirty);self.assertFalse(p.test_routes_btn.isEnabled())
        # Prevent the intentional unsaved-edit state from opening a modal confirmation in tearDown.
        p.pending_routes=[];p.route_errors=[];p.route_dirty=False;p._refreshing=True;p.proxy_text.clear();p._refreshing=False

    def test_connection_waiting_state_is_explicit_not_connected(self):
        p=self.page();s=AppleStore(self.window.db);cid=s.add_connection('owner@example.test');s.connection_state(cid,'waiting_sign_in','Complete Apple sign-in and two-factor verification in the browser')
        p.refresh();p.account.setCurrentIndex(p.account.findData(cid));p.account_changed();g.APP.processEvents()
        self.assertIn('Waiting for you to sign in',p.connection_info.text());self.assertTrue(p.verify_btn.isVisible());self.assertNotIn('Status: Connected',p.connection_info.text())


if __name__=='__main__':unittest.main(verbosity=2)
