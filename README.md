# Ah Pa Ta Tracker

Windows Apple Store order tracker with Gmail IMAP import, local SQLite storage, manual overrides, UPS API status, resilient large-account sync, and built-in over-the-air updates.

## Current stable version

**v1.0.1**

This repository is the stable update channel used by the app. The Windows release workflow reconstructs the source bundle, runs the automated tests, builds `AhPaTaTracker.exe`, computes its SHA-256 checksum, and publishes both files as a GitHub Release.

## Updating inside the app

Starting with v1.0.1, use **Check for Updates** in the app sidebar or **Settings > App updates**. The updater reads the latest stable GitHub Release, downloads the EXE and checksum, verifies SHA-256, closes the current app, replaces the EXE, and relaunches it.

Local orders and credentials are not stored in this repository and are not replaced by app updates.

## Source bundle

The connected publishing workflow stores the application source under `source_bundle/` as ordered base64 chunks. GitHub Actions verifies the bundle SHA-256 before extracting, testing, and building it. This keeps the release source snapshot exact while allowing automated publishing through the connected GitHub writer.

## Release process

For future updates, update the source bundle and release notes first, then update `version.json` last. Changing `version.json` triggers the Windows build/release workflow.
