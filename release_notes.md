# Ah Pa Ta Tracker v1.0.3 — updater, Apple sign-in, themes and proxy controls

- Replaces the fragile direct PyInstaller restart with a persistent native `AhPaTaTracker.exe` launcher. It validates its embedded app payload, clears stale PyInstaller/Python runtime variables, and waits for a tokenized startup acknowledgment that is written only after the database and main window initialize.
- Keeps update diagnostics across shutdown/restart and preserves the previous EXE on a startup failure without automatically downgrading after a possible database migration.
- Repairs the Apple Account workspace in dark mode and refines light-mode spacing, controls, table states, tabs, focus, disabled and feedback styling through the shared theme.
- Clarifies Apple Account connection states, automatic sign-in checks, browser-close/failure handling, two-factor instructions and reconnect recovery. Edge or Chrome is recommended; Brave remains experimental.
- Adds a Getting Started workflow and clearer action/status feedback throughout the Apple workspace and update flow.
- Renames Network routes to **Proxies**, adds explicit **Save Proxies**, preserves valid entries when other import rows are invalid, and stores credentials using the existing Windows user-bound protected vault.
- Adds per-proxy checkboxes, selection count, **Test Selected (N)**, stable proxy identities, bounded test concurrency, stop support, per-row results and no direct-network fallback during proxy tests.
- Preserves v1.0.2 safety rules: manual overrides remain highest priority, guest orders require account-list evidence before association, and Rebuild Cache cannot erase durable Apple job/verification history.

## Verification boundary

The release workflow runs offline core tests, Qt GUI checks and controlled browser-DOM scenarios before building/publishing Windows. Private Apple production pages, real sign-in/2FA, account association, cancellation and payment remain browser-assisted and are not claimed as live-verified. Start with one owned order.
