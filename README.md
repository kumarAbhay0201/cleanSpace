# CleanSpace

CleanSpace is a transparent, conservative Windows cleanup utility built with Python, FastAPI, HTML, CSS, and vanilla JavaScript.

## MVP status

The first slice supports scanning the current user's temporary directory and a dry-run or confirmed cleanup through approved target IDs. Scanning never deletes files. The cleaner skips symlinks, validates resolved paths, handles filesystem failures, and reports skipped items.

Packaged builds protect their temporary PyInstaller runtime directory from cleanup. This is required because the executable serves its dashboard assets from that extracted directory while it is running.

## Development

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

Run tests with `py -m pytest`.

## Build the Windows executable

On Windows, run:

```powershell
scripts\build_windows.bat
```

The output is `dist\CleanSpace.exe`. It starts a local server, opens the dashboard in the default browser, and includes the frontend assets. Keep the window open while using the app; closing the executable stops the local server.

## GitHub Pages download page

The repository root contains a static `index.html` intended for GitHub Pages. Publish from the repository root using **Settings → Pages → Deploy from a branch → main / root**.

The page download buttons point directly to `dist\CleanSpace.exe` on the `main` branch. For future releases, prefer attaching the executable to a GitHub Release and changing the page link to the release asset URL.
## Security

The browser sends cleanup target IDs, never paths. The backend resolves approved locations and checks every item remains inside its approved root. See [docs/security.md](docs/security.md).

## Roadmap

Browser caches, Recycle Bin inspection, richer progress reporting, settings persistence, and PyInstaller packaging are planned after the core safety model is extended and tested.

## License

MIT. See [LICENSE](LICENSE).
