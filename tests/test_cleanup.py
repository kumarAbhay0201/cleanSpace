from pathlib import Path

from app.cleaner.engine import CleanupEngine
from app.models.scan_result import CleanupItem, CleanupTarget


def test_dry_run_does_not_delete(tmp_path: Path):
    file_path = tmp_path / "cache.tmp"
    file_path.write_bytes(b"cache")
    target = CleanupTarget("test", "Test", "", str(tmp_path), items=[CleanupItem(str(file_path), 5)])
    result = CleanupEngine().clean([target], dry_run=True)
    assert result.bytes_removed == 5
    assert file_path.exists()


def test_cleanup_rejects_path_outside_target(tmp_path: Path):
    outside = tmp_path / "important.txt"
    outside.write_text("keep")
    target_root = tmp_path / "cache"
    target_root.mkdir()
    target = CleanupTarget("test", "Test", "", str(target_root), items=[CleanupItem(str(outside), 4)])
    result = CleanupEngine().clean([target])
    assert result.files_removed == 0
    assert outside.exists()
    assert "outside" in result.failed_items[0].reason.lower()


def test_cleanup_removes_file_and_continues(tmp_path: Path):
    file_path = tmp_path / "cache.tmp"
    file_path.write_bytes(b"cache")
    target = CleanupTarget("test", "Test", "", str(tmp_path), items=[CleanupItem(str(file_path), 5)])
    result = CleanupEngine().clean([target])
    assert result.files_removed == 1
    assert not file_path.exists()
