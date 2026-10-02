from dataclasses import dataclass, field
from typing import Any


@dataclass
class FailedItem:
    path: str
    reason: str


@dataclass
class CleanupResult:
    status: str
    bytes_removed: int = 0
    files_removed: int = 0
    failed_items: list[FailedItem] = field(default_factory=list)
    dry_run: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "bytes_removed": self.bytes_removed,
            "files_removed": self.files_removed,
            "files_skipped": len(self.failed_items),
            "failed_items": [item.__dict__ for item in self.failed_items],
            "dry_run": self.dry_run,
        }
