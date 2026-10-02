import shutil
from pathlib import Path


def storage_info() -> dict[str, int | str]:
    root = Path.home().anchor or "/"
    usage = shutil.disk_usage(root)
    return {"path": root, "total": usage.total, "used": usage.used, "free": usage.free}
