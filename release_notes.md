# Ah Pa Ta Tracker v1.0.4 — Apple Account workflow, jobs and proxy management

- Fixes the Apple Account connection handoff that could leave v1.0.3 sitting on Apple's guest **Find your order** page. The tracker now selects an explicit Apple Account sign-in branch when Apple exposes one, waits for Apple's own password/passkey/2FA flow, probes saved sessions, and does not mark the guest page as authenticated.
- Simplifies Apple order actions to **select orders → choose action → START**, with a connected Apple Account required before queueing authenticated work and frozen target IDs at confirmation.
- Preserves order selection by stable IDs across refresh/sort/filter operations and adds Shift-click range selection in order tables.
- Expands the Proxies tab with Add, Edit, Delete selected, Delete all, Enable/Disable, Select all, Clear selection, Save and exact **Test Selected (N)** controls.
- Adds controlled proxy failover for transport/proxy failures before a mutation is submitted. Explicit Apple 429/throttling still uses cooldown/backoff and never rotates routes to bypass the throttle.
- Adds Jobs/results cleanup: Remove selected, Remove completed and guarded Stop-and-Remove. Removing a job only archives local history; it does not reverse completed Apple actions, and audit/task records remain available.
- Enlarges Apple batch review/mapping/detail dialogs and improves column sizing so important order information is visible without needless horizontal scrolling.
- Treats already-associated orders idempotently and keeps expected failures—session expiry, missing phones, ineligibility, timeouts, transport errors, throttling and uncertain mutations—as recoverable job outcomes instead of application crashes.
- Retains the existing authenticated Apple observation precedence below manual overrides and above email/carrier sources.
- Keeps Apple passwords, passkeys, 2FA codes and raw payment credentials on Apple's visible page. Cancellation/payment remain guarded browser-assisted operations with post-action reconciliation.

## Verification boundary

The release workflow runs offline core tests, Windows Qt GUI checks and controlled browser-DOM scenarios before building/publishing. Private Apple production pages, a real user sign-in/2FA session, association of an owned guest order, real cancellation and real payment changes cannot be exercised by CI and require user validation. Unknown Apple layouts pause for handoff rather than being reported as success. Start with one owned order before authorizing a large batch.