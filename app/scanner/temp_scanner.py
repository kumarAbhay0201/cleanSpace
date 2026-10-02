from pathlib import Path

from app.models.scan_result import CleanupItem, CleanupTarget
from app.utils.filesystem import iter_safe_entries


def scan_target(target: CleanupTarget, root: Path | None = None) -> CleanupTarget:
    scan_root = root or Path(target.location)
    target.items.clear()
    for path in iter_safe_entries(scan_root):
        try:
            stat = path.stat()
        except (OSError, PermissionError):
            continue
        target.items.append(CleanupItem(str(path), stat.st_size, path.is_dir()))
    return target
