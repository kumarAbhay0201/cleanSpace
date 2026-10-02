from pathlib import Path
from collections.abc import Iterator


def iter_safe_entries(root: Path, excluded_roots: tuple[Path, ...] = ()) -> Iterator[Path]:
    if not root.exists() or not root.is_dir():
        return
    for entry in root.iterdir():
        try:
            if entry.is_symlink():
                continue
            resolved_entry = entry.resolve(strict=False)
            if any(resolved_entry == excluded or excluded in resolved_entry.parents for excluded in excluded_roots):
                continue
            yield entry
            if entry.is_dir():
                yield from iter_safe_entries(entry, excluded_roots)
        except (OSError, PermissionError):
            continue


def is_within(path: Path, root: Path) -> bool:
    try:
        return path.resolve(strict=False).is_relative_to(root.resolve(strict=False))
    except (OSError, RuntimeError):
        return False
