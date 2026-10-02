import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.api.scan import SCANS, start_scan
from app.api.system import storage_info
from app.cleaner.engine import CleanupEngine
from app.config.cleanup_targets import get_target
from app.recycle_bin.manager import empty_recycle_bin, get_recycle_bin_info
from app.utils.size import format_bytes

app = FastAPI(title="CleanSpace", version="0.1.0")
PROJECT_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
FRONTEND = PROJECT_ROOT / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


class CleanupRequest(BaseModel):
    targets: list[str] = Field(min_length=1)
    dry_run: bool = False


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")


@app.get("/api/system/storage")
def system_storage() -> dict:
    return storage_info()


@app.post("/api/scan")
def scan() -> dict:
    return start_scan().as_dict()


@app.get("/api/scan/{scan_id}")
def scan_status(scan_id: str) -> dict:
    if scan_id not in SCANS:
        raise HTTPException(status_code=404, detail="Scan not found")
    return SCANS[scan_id].as_dict()


@app.post("/api/cleanup")
def cleanup(request: CleanupRequest) -> dict:
    targets = []
    for target_id in request.targets:
        target = get_target(target_id)
        if target is None or not target.enabled or target.safety != "safe":
            raise HTTPException(status_code=400, detail=f"Unsupported cleanup target: {target_id}")
        targets.append(target)
    latest = next(reversed(SCANS.values()), None)
    if latest:
        by_id = {target.id: target for target in latest.categories}
        targets = [by_id[target.id] for target in targets if target.id in by_id]
    return CleanupEngine().clean(targets, dry_run=request.dry_run).as_dict()


@app.get("/api/recycle-bin")
def recycle_bin() -> dict:
    return get_recycle_bin_info()


@app.post("/api/recycle-bin/empty")
def recycle_bin_empty() -> dict:
    if not empty_recycle_bin():
        raise HTTPException(status_code=500, detail="Windows could not empty the Recycle Bin")
    return {"status": "complete", **get_recycle_bin_info()}


@app.get("/api/settings")
def settings() -> dict:
    return {"theme": "dark", "include_browser_cache": False, "notifications": True}


@app.get("/api/health")
def health() -> dict:
    return {"status": "ready", "platform": sys.platform, "formatted_zero": format_bytes(0)}
