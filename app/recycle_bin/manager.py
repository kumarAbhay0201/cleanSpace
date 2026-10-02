import ctypes
import sys
from ctypes import wintypes


class SHQUERYRBINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD), ("i64Size", ctypes.c_longlong), ("i64NumItems", ctypes.c_longlong)]


def get_recycle_bin_info() -> dict[str, int | str | bool]:
    if sys.platform != "win32":
        return {"supported": False, "total_size": 0, "item_count": 0, "message": "Recycle Bin scanning is Windows-only."}
    info = SHQUERYRBINFO(ctypes.sizeof(SHQUERYRBINFO), 0, 0)
    result = ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(info))
    if result != 0:
        return {"supported": True, "total_size": 0, "item_count": 0, "message": "Windows could not inspect the Recycle Bin."}
    return {"supported": True, "total_size": info.i64Size, "item_count": info.i64NumItems, "message": "Size reported by the Windows Recycle Bin."}


def empty_recycle_bin() -> bool:
    if sys.platform != "win32":
        return False
    result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000001)
    return result == 0
