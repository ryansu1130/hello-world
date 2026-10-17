# Ah Pa Ta Tracker v1.0.1

- Adds built-in over-the-air updates from GitHub Releases.
- Adds manual **Check for Updates** in the sidebar and Settings.
- Adds optional automatic stable-update checking on startup.
- Downloads and verifies the Windows EXE with a published SHA-256 checksum before installation.
- Replaces the EXE only after the running app exits, keeps a previous-EXE backup, then relaunches automatically.
- Preserves the v1.0.0 resilient Gmail sync, UPS API tracking, manual overrides, and iPhone Duo delivery-range parsing.
- Does not replace the local order database or Credential Manager secrets.