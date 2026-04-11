import sys

if sys.platform == "win32":
    from ctypes import windll

    kernel32 = windll.kernel32
    user32 = windll.user32
    SW_HIDE = 0
    SW_SHOW = 5

    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        if len(sys.argv) <= 1:
            user32.ShowWindow(hWnd, SW_HIDE)
        else:
            user32.ShowWindow(hWnd, SW_SHOW)

    if len(sys.argv) > 1:
        sys.stdin = open("CONIN$", "r", encoding="utf-8", errors="replace")
        sys.stdout = open("CONOUT$", "w", encoding="utf-8", errors="replace", buffering=1)
        sys.stderr = open("CONOUT$", "w", encoding="utf-8", errors="replace", buffering=1)
