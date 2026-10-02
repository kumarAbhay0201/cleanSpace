# Security model

CleanSpace is deliberately conservative.

- The frontend submits target IDs only. It cannot submit arbitrary deletion paths.
- The backend owns the approved target registry and resolves locations locally.
- Scanners skip symbolic links and recursively traverse only known directories.
- Cleanup resolves each path and compares it to the approved root using `Path.is_relative_to`, never a string prefix.
- The target directory itself is never removed.
- Missing, locked, and permission-denied entries become reported skipped items.
- Logs and API responses do not include file contents or credentials.

The current MVP exposes only the user's temporary directory. Windows-specific targets will be added only with dedicated tests and documentation.
