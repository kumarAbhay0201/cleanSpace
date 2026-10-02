from uuid import uuid4

from app.config.cleanup_targets import target_definitions
from app.models.scan_result import ScanResult
from app.scanner.temp_scanner import scan_target

SCANS: dict[str, ScanResult] = {}


def start_scan() -> ScanResult:
    scan = ScanResult(scan_id=uuid4().hex, status="scanning")
    for target in target_definitions().values():
        scan_target(target)
        scan.categories.append(target)
    scan.status = "complete"
    scan.total_size = sum(item.size for target in scan.categories for item in target.items)
    scan.total_files = sum(target.file_count for target in scan.categories)
    SCANS[scan.scan_id] = scan
    return scan
