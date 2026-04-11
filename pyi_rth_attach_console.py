"""
PyInstaller runtime hook for html2pdf.

Dieser Hook wird beim Start der mit PyInstaller gebauten Executable ausgeführt.
Er ist notwendig, um das Verhalten der EXE zwischen GUI- und CLI-Start zu trennen:

- Bei einem normalen Doppelklick ohne zusätzliche Argumente soll die GUI starten
  und keine sichtbare Konsole öffnen.
- Bei CLI-Argumenten wie `--help` oder `--input` soll eine Konsole sichtbar
  sein, damit die Ausgabe lesbar ist.
- Zusätzlich werden die Standard-Streams auf UTF-8 gesetzt, damit die Hilfe- und
  Fehlermeldungen mit Sonderzeichen korrekt dargestellt werden.

Der Hook wird von `html2pdf.spec` als `runtime_hooks=[str(runtime_hook)]`
 eingebunden. Wird die Datei gelöscht, bricht der Build, weil der Runtime-Hook
nicht mehr gefunden wird.
"""

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
