# Ah Pa Ta Tracker v1.0.2 - Apple Account workspace

- Adds an Apple Account workspace with isolated visible Edge/Chrome sessions and experimental Brave support.
- Imports exact-alias phone candidates from many JSON files, retaining provenance and per-order verification. Payment objects are not imported.
- Shows Phone number(s) directly below Alias email in order details.
- Adds confirmed, durable association/refresh/cancellation/payment job interfaces, pause/resume/stop/reconcile controls and sanitized result export.
- Adds authenticated Apple observations below manual overrides and above existing email/carrier reconciliation.
- Preserves Gmail sync, UPS tracking, manual edits, archives, exports, calendar and existing data location; backs up before additive migration.
- Includes stable proxy routes, encrypted Windows app-session storage and cooldowns without bypass behavior.
- Requires signed-in account-list evidence before marking a new guest-order association or verifying its phone candidate.
- Protects durable Apple job, submission and verification history from Rebuild Cache; email can still be refreshed with Full Account Sync or Refresh Details.
- Stops order-detail refresh timers when their dialogs close, preventing background reads after database shutdown.

## Important limitations

Private Apple production flows have not been live-verified. Unknown pages, sign-in,
2FA or uncertainty require browser handoff. Cancellation and payment final submission
are browser-assisted; this release does not automatically apply one raw card across
a batch. A method update is not proof of payment clearance. Brave and dynamic Apple
page layouts require validation in the user's environment. No real orders/payments
were changed in tests.

Read README.md and REQUIREMENTS_STATUS.md before using Apple actions. Start with one
owned order. A release is published only after its configured Windows CI gates pass.
