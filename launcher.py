import threading
import webbrowser

import uvicorn

from app.main import app


HOST = "127.0.0.1"
PORT = 8765


def run_server() -> None:
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    webbrowser.open(f"http://{HOST}:{PORT}")
    server_thread.join()
