"""
cli_app.py – Einstiegspunkt für die CLI von html2pdf 0.5.0
"""

import sys

from html2pdf.cli.runner import main as run_cli
from html2pdf.gui.gui_app import run_gui
from html2pdf.version import __version__


def cli_or_gui():
    """
    Entscheidet, ob CLI oder GUI gestartet wird.

    Regeln:
    - Wenn KEINE Argumente übergeben wurden → GUI starten
    - Wenn Argumente übergeben wurden → CLI starten
    """

    # sys.argv enthält IMMER mindestens 1 Element (das Skript selbst)
    if len(sys.argv) == 1:
        return "gui"

    return "cli"


def main():
    """
    Haupt-Einstiegspunkt für html2pdf.
    Wird von __main__.py und PyInstaller genutzt.
    """

    mode = cli_or_gui()

    if mode == "gui":
        run_gui()
    else:
        run_cli()