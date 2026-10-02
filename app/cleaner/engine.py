from pathlib import Path

from app.models.cleanup_result import CleanupResult, FailedItem
from app.models.scan_result import CleanupTarget
from app.utils.filesystem import is_within


class CleanupEngine:
    def clean(self, targets: list[CleanupTarget], dry_run: bool = False) -> CleanupResult:
        result = CleanupResult(status="dry_run" if dry_run else "complete", dry_run=dry_run)
        for target in targets:
            root = Path(target.location)
            for item in target.items:
                path = Path(item.path)
                if not is_within(path, root) or path == root:
                    result.failed_items.append(FailedItem(str(path), "Path is outside the approved target"))
                    continue
                try:
                    if not path.exists():
                        result.failed_items.append(FailedItem(str(path), "File disappeared before cleanup"))
                        continue
                    if dry_run:
                        result.bytes_removed += item.size
                        result.files_removed += 1 if not item.is_directory else 0
                        continue
                    if item.is_directory:
                        self._remove_directory_contents(path)
                    else:
                        path.unlink()
                    result.bytes_removed += item.size
                    result.files_removed += 1 if not item.is_directory else 0
                except (OSError, PermissionError) as exc:
                    result.failed_items.append(FailedItem(str(path), self._reason(exc)))
        return result

    @staticmethod
    def _remove_directory_contents(directory: Path) -> None:
        for child in directory.iterdir():
            if child.is_symlink():
                continue
            if child.is_dir():
                CleanupEngine._remove_directory_contents(child)
                child.rmdir()
            else:
                child.unlink()

    @staticmethod
    def _reason(error: OSError) -> str:
        if getattr(error, "winerror", None) in (5, 32):
            return "Access denied or file is currently in use"
        return str(error) or "Filesystem rejected the operation"
