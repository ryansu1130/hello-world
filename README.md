# Ah Pa Ta Tracker v1.0.5

Ah Pa Ta Tracker is a Windows Apple order tracker with Gmail import, local SQLite storage, UPS tracking, manual overrides, Apple Account browser-assisted workflows, phone mapping, proxy management, durable Apple jobs and built-in GitHub Release updates.

## v1.0.5 Apple Account connection recovery

The Apple Account workspace now distinguishes a guest **Find your order** page
from Apple's actual account sign-in, password/passkey/2FA challenges, and a
signed-in order listing. `Connected` requires verified account/order-list
conditions: a browser opening by itself never counts as authenticated.

To complete a real sign-in on Windows, open **Apple Account → Connection**,
select the owned Apple Account and click **Connect Apple Account**. If Apple
shows **Find your order**, click **Open Apple Account Sign-in**. Complete Apple's
login and any verification in the **dedicated** browser (not in this app).
Then click **Open Order Listing** or **Check Session**. If the account identity
is hidden, explicitly confirm the visible signed-in Apple Account; a mismatched
visible identity always blocks jobs. Use **Reconnect**, **Cancel connection**,
or **Forget saved session** as appropriate. Start with one owned order.

**Live-production boundary:** A real Apple login, live order association,
status refresh, cancellation and payment changes cannot be validated using
isolated CI fixtures. No such production success is claimed until verified
by the user. The new 236-unit test and 16-browser-scenario gate, together with
Windows GUI checks, cover the application contracts and error handling only.

The release also adds explicit **Test All Enabled** proxy testing, a guarded
**Clear finished history** control (audit retained), improved connection
feedback across tabs and a more adaptive Apple batch review dialog.

## v1.0.4 production-readiness update

v1.0.4 concentrates on the Apple Account workflow shown in the supplied v1.0.3 screenshots.

1. **Apple Account sign-in handoff fixed.** The dedicated browser no longer treats the guest "Find your order" branch as a completed connection. When Apple exposes an explicit Apple Account sign-in control, the tracker selects that branch, then waits for the user to complete Apple's own password/passkey/two-factor flow. A saved authenticated session is probed before asking the user to sign in again. The tracker only enables authenticated order actions after account/session verification.
2. **One simpler Apple action flow.** In the normal order views, select one or many orders, choose Link / Refresh / Cancel / Update payment, then press one clear **START** button. The confirmed target IDs are frozen for the job. Apple Account connection is a prerequisite rather than an implementation detail buried inside job results.
3. **Better large-order selection.** Checkbox selections now survive sorting/filter/page refreshes by stable order ID, and Shift-click selects a visible contiguous range from the previous anchor. Existing select-all/filter workflows remain available.
4. **Fuller proxy management.** The Proxies tab now supports Add, Edit, Delete selected, Delete all, Enable selected, Disable selected, Select all, Clear selection, Save and exact **Test Selected (N)** behavior. Credentials remain masked and protected.
5. **Safe route failover.** Enabled healthy proxy routes may be selected automatically after a transport/proxy failure before a mutation is submitted. Explicit Apple throttling/429 responses still use cooldown/backoff and do **not** rotate routes as a way around Apple's controls.
6. **Job cleanup.** Jobs/results now supports removing selected history, removing completed jobs, and Stop-and-Remove for active work. Removal is a local archive operation; it never claims to undo an Apple action that already completed. Audit/task records are retained.
7. **Larger review/details dialogs.** Batch review and mapping/detail dialogs open much larger, use the available desktop area, and reduce unnecessary horizontal scrolling.
8. **Idempotent/defensive execution.** An order that is already associated is handled as `already_associated`, refreshed, and does not crash the batch. Transport failures, timeouts, throttling, missing phone data, session expiry, ineligibility, uncertain mutations and other expected outcomes remain job states/results instead of process crashes.

## Intended workflow

1. **Connect Apple Account.** Add the destination Apple Account and press **Connect Apple Account**. Sign in and complete two-factor verification on Apple's visible page. The tracker does not collect the Apple password or verification code.
2. **Import data.** Import JSON phone/profile files and, if desired, proxy/network-route data. Multiple phone candidates stay scoped to the matching alias/order until one is verified for that specific order.
3. **Select orders.** Check one order, Ctrl-click/toggle individual selections, Shift-click a range, or use the existing all/filtered selection controls.
4. **Choose an Apple action.** Link guest order, Refresh, Cancel eligible order/item, or Update payment when Apple exposes that workflow.
5. **Press START.** Review the frozen Apple Account/action/targets and confirm. The durable job runner executes eligible work and reports progress, cooldowns, handoffs and per-order outcomes.
6. **Review Jobs.** Pause/resume/stop/retry where appropriate, remove old jobs from the main view, and inspect sanitized results without losing the audit record.

## Apple workflow boundary

Apple's current Shopping Help says Order Listing is the signed-in location for viewing/editing orders, that guest orders must be added to an Apple Account to make changes online, and that adding a guest order includes verifying the phone number used to place it. The application therefore uses a visible Apple browser workflow rather than fabricating a private API.

Apple passwords, passkeys, 2FA codes and raw payment credentials remain on Apple's page. Cancellation and payment changes are guarded, eligibility is re-read, and uncertain mutation results are reconciled before any retry. A payment-method update is not treated as proof that payment has cleared.

Private Apple production pages and user credentials are not exercised by automated CI. Start with one owned order and validate the live page flow before authorizing a large batch. Unknown Apple layouts stop for a browser/user handoff instead of being guessed as successful.

## Status precedence

Displayed tracker status continues to use:

1. Active manual override.
2. Latest successful authenticated Apple observation.
3. Existing lower-priority email/carrier sources in their prior relative order.

A failed Apple refresh does not erase the last successful Apple observation.

## Proxy behavior

Proxies are optional network routes for Apple browser work; they are not merely a login setting. A healthy enabled route can be used after a genuine transport/proxy failure. Explicit Apple throttling, security challenges and verification limits are different failure classes: the tracker pauses/cools down, respects retry timing, and does not rapidly rotate proxies or clear cookies to bypass them.

A proxy health test proves only the configured route reached its test destination. It does not prove Apple sign-in or order access.

## Data and secrets

The update keeps `%LOCALAPPDATA%\AppleOrderTracker\orders.db`, Gmail/UPS settings, manual edits, archives, exports, JSON phone mappings and Apple job history. Schema v3 is additive. Proxy/session secrets use the existing Windows user-bound protected vault; passwords, cookies, full payment-card details and CVV are not written to normal logs or plaintext SQLite fields.

## Update channel

The application reads stable releases from `ryansu1130/hello-world`. A release is installable only when both `AhPaTaTracker.exe` and `AhPaTaTracker.exe.sha256` are present and the checksum verifies.

The Windows release workflow reconstructs the stable source, applies the version overlay, runs offline/core, Qt and controlled-browser gates, builds the PyInstaller payload plus persistent native launcher, generates the public SHA-256 and publishes only after all gates pass.

## Local build

On Windows run `build_windows.bat`. It runs the configured validation gates and creates `dist\AhPaTaTracker.exe`. Normal users should use **Check for Updates** after v1.0.5 is published.