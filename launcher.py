import threading
import webbrowser
from pathlib import Path

import uvicorn

from app.main import app


HOST = "127.0.0.1"
PORT = 8765


def run_server(log_path: Path) -> None:
    try:
        uvicorn.run(app, host=HOST, port=PORT, log_config=None, access_log=False)
    except Exception as error:
        log_path.write_text(f"CleanSpace server failed: {error!r}\n", encoding="utf-8")


if __name__ == "__main__":
    log_path = Path.home() / "CleanSpace-startup.log"
    try:
        server_thread = threading.Thread(target=run_server, args=(log_path,), daemon=True)
        server_thread.start()
        webbrowser.open(f"http://{HOST}:{PORT}")
        server_thread.join()
    except Exception as error:
        log_path.write_text(f"CleanSpace startup failed: {error!r}\n", encoding="utf-8")
        raise
