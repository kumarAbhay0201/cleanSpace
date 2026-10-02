from pathlib import Path

from app.models.scan_result import CleanupTarget
from app.scanner.temp_scanner import scan_target


def test_scanner_counts_files_without_following_symlinks(tmp_path: Path):
    (tmp_path / "one.tmp").write_bytes(b"123")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "two.tmp").write_bytes(b"12345")
    target = CleanupTarget("test", "Test", "", str(tmp_path))
    scan_target(target)
    assert target.file_count == 2
    assert target.size == 8
