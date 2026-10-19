# Ah Pa Ta Tracker

Windows Apple Store order tracker with Gmail IMAP, local SQLite storage, UPS API,
manual overrides, selected exports and in-app updates through this repository.

## Install or update

From v1.0.1 or newer, choose **Check for Updates** in the app sidebar or Settings.
The tracker downloads the latest stable Windows executable, verifies its SHA-256,
then replaces and relaunches the application. No source download or local build
is needed. Existing orders and settings remain in their current local location.

For a new installation, download **AhPaTaTracker.exe** from
[the latest stable release](https://github.com/ryansu1130/hello-world/releases/latest).
Microsoft Edge or Google Chrome must be installed for the Apple Account workspace.

## v1.0.2: Apple Account workspace

This source revision adds exact-alias phone mappings, isolated browser sign-in,
confirmed durable Apple action jobs and authenticated Apple observations. Manual
overrides remain highest priority. **Apple actions are browser-assisted and private
production pages were not live-verified during development.** Cancellation/payment
final submissions can require a user handoff. No raw card batch-reuse feature is
claimed. The source README and REQUIREMENTS_STATUS.md explain limitations.

The latest successfully published stable release is the source of truth for
**Check for Updates**. A new version.json commit is not itself a successful release.

## Publishing and OTA

The Windows Actions workflow reconstructs the exact source snapshot from ordered
base64 files in `source_bundle/`, checks its SHA-256, runs core/Qt/controlled-browser
tests, packages the Windows EXE and creates a draft release. It publishes only after
both `AhPaTaTracker.exe` and `AhPaTaTracker.exe.sha256` are uploaded. Existing releases
are not overwritten. See the Actions result for the actual build outcome.

Starting with v1.0.1 the app reads the latest stable release, downloads its EXE and
checksum, verifies the bytes, closes the old app and launches the replacement. The
local order database and credential/session storage are not release assets.

## Source, tests and privacy

`source_bundle/manifest.json` declares the archive checksum and part count. Decode
parts in numbered order and unzip to read the source, tests and documentation.
Only curated application source, synthetic tests, docs and app icons are published.
Do not add your Profiles.json, order emails, database, Apple cookies, API keys,
proxy credentials or payment data to this repository.
