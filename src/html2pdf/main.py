"""
Einstiegspunkt: entscheidet zwischen GUI und CLI.
"""

import sys
from html2pdf.cli.cli_app import run_cli
from html2pdf.gui.gui_app import run_gui

def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()
