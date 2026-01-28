import win32gui
import win32process
import psutil

def get_active_window_context() -> dict:
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    process_name = None
    try:
        process = psutil.Process(pid)
        process_name = process.name()
    except Exception:
        pass

    return {
        "window_title": window_title,
        "process_name": process_name
    }
