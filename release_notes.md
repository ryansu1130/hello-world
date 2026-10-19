# Ah Pa Ta Tracker v1.0.6 — Reliable Windows in-app updates

- Fixes the reported updater failure: the existing EXE was left locked after the app PID exited, so the old helper could neither overwrite nor restore it.
- Tracks both the application PID and the independent persistent native-launcher PID; waits for them to exit before installing.
- Replaces the old single-attempt CMD copy-and-rollback logic with a standalone PowerShell helper that stages the verified download on the installed volume and uses atomic `File.Replace` with bounded retries for Windows file locks.
- Computes SHA-256 through built-in .NET cryptography (without assuming Get-FileHash exists) and checks the downloaded checksum again, preserves the original EXE if replacement cannot occur, retains the verified download on failure and reports precise update-stage errors.
- Waits for the new native launcher to finish its startup acknowledgment. If startup is uncertain after replacement, retains the previous EXE without automatically launching an older binary against a potentially migrated database.
- Adds Windows integration regressions using actual Windows executables, including a simulated file lock and failed replacement preservation.
- Preserves Apple Account sign-in recovery, order association controls, jobs, proxy selection, Gmail/UPS tracking, and all user data from v1.0.5.

## Existing v1.0.4/v1.0.5 installations

The old installer helper is embedded in the installed program and cannot be retroactively fixed by publishing a release. If Check for Updates fails with "file is being used by another process", close all tracker processes and manually replace only the installed `AhPaTaTracker.exe` with this release's verified executable, ideally after a Windows restart. The local database is stored separately under `%LOCALAPPDATA%\AppleOrderTracker` and must be left untouched. Subsequent releases can use the fixed update helper.

## Verification limits

Windows CI runs offline core tests, Qt GUI checks, controlled browser fixtures, a locked-file updater integration test, and the native-launcher build before publishing. Actual file locks and endpoint security software on a user's PC can differ from CI. Live Apple login/order actions remain browser-assisted and require user validation.