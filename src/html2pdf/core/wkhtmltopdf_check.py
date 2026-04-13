"""
Prüft, ob wkhtmltopdf verfügbar ist.
Bevorzugt die interne portable Version (html2pdf/bin/wkhtmltopdf.exe).
"""

from pathlib import Path
import shutil
import sys


def _get_base_path() -> Path:
    """Ermittelt den Basisordner für PyInstaller oder Entwicklungsmodus."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "html2pdf"
    else:
        return Path(__file__).resolve().parent.parent


def find_wkhtmltopdf() -> str | None:
    """Sucht zuerst die interne portable Version, danach die Systeminstallation."""
    base = _get_base_path()
    internal_exe = base / "bin" / "wkhtmltopdf.exe"

    # Debug-Ausgabe
    # print("DEBUG: Suche wkhtmltopdf in:", internal_exe)

    # 1. Interne Version
    if internal_exe.is_file():
        # print("DEBUG: Interne wkhtmltopdf.exe gefunden:", internal_exe)
        return str(internal_exe)

    # 2. Systeminstallation
    system_exe = shutil.which("wkhtmltopdf")
    # print("DEBUG: Systeminstallation:", system_exe)

    if system_exe:
        return system_exe

    return None


def ensure_wkhtmltopdf_or_raise() -> str:
    """Gibt den Pfad zurück oder wirft eine Exception."""
    path = find_wkhtmltopdf()
    # print("DEBUG: Finaler wkhtmltopdf-Pfad:", path)

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