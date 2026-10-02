# Cleanup targets

## User Temporary Files

**Location:** `%TEMP%`

**Contains:** Temporary files created by Windows and applications.

**Cleanup effect:** Some applications may recreate these files. Files in use are skipped.

**Does not remove:** The temp directory itself, symbolic links, or files outside the approved root.

**Privileges:** Normal user permissions are used in the MVP.
