import os
from pathlib import Path

from app.models.scan_result import CleanupTarget


def _user_temp() -> Path:
    return Path(os.environ.get("TEMP", Path.home() / "AppData" / "Local" / "Temp"))


def target_definitions() -> dict[str, CleanupTarget]:
    temp = _user_temp()
    return {
        "user_temp": CleanupTarget(
            id="user_temp",
            name="User Temporary Files",
            description="Temporary files created by Windows and applications.",
            location=str(temp),
        ),
    }


def get_target(target_id: str) -> CleanupTarget | None:
    return target_definitions().get(target_id)
