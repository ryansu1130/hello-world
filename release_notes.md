# Ah Pa Ta Tracker v1.0.5 — Apple Account sign-in and workflow recovery

- Separates Apple Account sign-in, password/passkey challenges, Apple 2FA, page-loading delays, and guest Find Your Order from real verified account state.
- Opens the dedicated Apple Account sign-in branch from guest lookup instead of waiting indefinitely on a guest-order spinner.
- Detects Apple-hosted embedded verification controls without reading any form field values.
- Verifies a signed-in Apple order listing and the selected Apple Account identity before permitting authenticated order actions; unknown and mismatched states remain blocked.
- Adds clearer Open Apple Account Sign-in, Open Order Listing, Check Session, Reconnect, Cancel Connection and Forget Saved Session controls, with browser-close recovery.
- Continues checking sign-in while another tracker tab is visible.
- Adds explicit Test All Enabled Proxies (without silently falling back to Direct), and Clear Finished Job History with audit preservation.
- Improves batch-review table sizing and responsive dialog behavior.
- Preserves v1.0.4 JSON phone mapping, bulk START, account-evidence guards, proxy CRUD, selected route tests, cooldowns, verified/uncertain action semantics, jobs, Gmail sync, UPS tracking, status priorities and native OTA launcher.

## Verification boundary

The release pipeline runs 236 offline core checks plus Windows Qt tests and 16 controlled Chromium DOM scenarios. Controlled fixtures are NOT Apple's production environment. Real Apple Account login, 2FA, association, cancellation, payment and order-status updates require manual validation by the user in their dedicated Apple browser. The app never collects passwords, 2FA codes or full card data.

The Windows v1.0.5 validation includes a corrected proxy-selection GUI regression that refreshes the saved route list through the existing workspace refresh method. The candidate must pass the packaged Windows release gates before it is promoted to stable.
