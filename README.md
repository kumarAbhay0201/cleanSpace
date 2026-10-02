# CleanSpace

CleanSpace is a transparent, conservative Windows cleanup utility built with Python, FastAPI, HTML, CSS, and vanilla JavaScript.

## MVP status

The first slice supports scanning the current user's temporary directory and a dry-run or confirmed cleanup through approved target IDs. Scanning never deletes files. The cleaner skips symlinks, validates resolved paths, handles filesystem failures, and reports skipped items.

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

The repository root contains a static `index.html` intended for GitHub Pages. Before publishing, replace `YOUR_USERNAME/clean-space` in that file with the real GitHub repository path. Publish from the repository root using **Settings → Pages → Deploy from a branch → main / root**.

Upload `dist\CleanSpace.exe` to a GitHub Release named `v0.1.0`. The page download buttons point to the latest release asset at `releases/latest/download/CleanSpace.exe`.
## Security

The browser sends cleanup target IDs, never paths. The backend resolves approved locations and checks every item remains inside its approved root. See [docs/security.md](docs/security.md).

## Roadmap

Browser caches, Recycle Bin inspection, richer progress reporting, settings persistence, and PyInstaller packaging are planned after the core safety model is extended and tested.

## License

MIT. See [LICENSE](LICENSE).
