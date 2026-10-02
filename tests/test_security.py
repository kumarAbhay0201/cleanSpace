from pathlib import Path

from app.utils.filesystem import is_within


def test_path_validation_uses_resolved_paths(tmp_path: Path):
    root = tmp_path / "approved"
    root.mkdir()
    assert is_within(root / "nested" / "file.tmp", root)
    assert not is_within(tmp_path / "other" / "file.tmp", root)
