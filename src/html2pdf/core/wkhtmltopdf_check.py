"""
Prüft, ob wkhtmltopdf verfügbar ist.
Bevorzugt die interne portable Version (html2pdf/bin/wkhtmltopdf.exe).
"""

from pathlib import Path
import shutil
import sys


def _get_base_path() -> Path:
    """
    Ermittelt den Basisordner, abhängig davon,
    ob das Programm als PyInstaller-EXE läuft oder normal.
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller: extrahierter Temp-Ordner
        return Path(sys._MEIPASS) / "html2pdf"
    else:
        # Entwicklungsumgebung: src/html2pdf/
        return Path(__file__).resolve().parent.parent


def find_wkhtmltopdf() -> str | None:
    """
    Sucht zuerst die interne portable Version,
    danach die Systeminstallation.
    """
    base = _get_base_path()
    internal_exe = base / "bin" / "wkhtmltopdf.exe"

    # 1. Interne Version
    if internal_exe.is_file():
        return str(internal_exe)

    # 2. Systeminstallation
    system_exe = shutil.which("wkhtmltopdf")
    if system_exe:
        return system_exe

    return None


def ensure_wkhtmltopdf_or_raise() -> str:
    """
    Gibt den Pfad zu wkhtmltopdf zurück oder wirft eine Exception
    mit einer klaren Fehlermeldung.
    """
    path = find_wkhtmltopdf()
    if path is None:
        raise RuntimeError(
            "wkhtmltopdf wurde nicht gefunden.\n\n"
            "html2pdf erwartet entweder:\n"
            "- die interne portable Version im Ordner html2pdf/bin/\n"
            "  (wkhtmltopdf.exe + libwkhtmltox.dll)\n"
            "ODER\n"
            "- eine installierte Version im PATH.\n\n"
            "Bitte prüfen Sie die Installation oder die Projektstruktur."
        )
    return path