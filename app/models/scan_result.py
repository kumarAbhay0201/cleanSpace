from dataclasses import dataclass, field
from typing import Any


@dataclass
class CleanupItem:
    path: str
    size: int
    is_directory: bool = False


@dataclass
class CleanupTarget:
    id: str
    name: str
    description: str
    location: str
    safety: str = "safe"
    enabled: bool = True
    items: list[CleanupItem] = field(default_factory=list)

    @property
    def size(self) -> int:
        return sum(item.size for item in self.items)

    @property
    def file_count(self) -> int:
        return sum(1 for item in self.items if not item.is_directory)

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "safety": self.safety,
            "enabled": self.enabled,
            "size": self.size,
            "file_count": self.file_count,
            "items": [{"path": item.path, "size": item.size, "is_directory": item.is_directory} for item in self.items[:100]],
        }


@dataclass
class ScanResult:
    scan_id: str
    status: str
    total_size: int = 0
    total_files: int = 0
    categories: list[CleanupTarget] = field(default_factory=list)
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "scan_id": self.scan_id,
            "status": self.status,
            "total_size": self.total_size,
            "total_files": self.total_files,
            "categories": [category.summary() for category in self.categories],
            "error": self.error,
        }
