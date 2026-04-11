"""
CLI-Frontend für automatisierte Verarbeitung.
"""

import argparse
import itertools
import threading
import sys
import time
from pathlib import Path

from html2pdf.core.file_utils import resolve_input_path, build_output_path
from html2pdf.core.converter import convert_single_html
from html2pdf.core.logger import setup_logger
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__


# ---------------------------------------------------------
# Spinner-Funktion
# ---------------------------------------------------------
def start_spinner(stop_event, prefix=""):
    spinner = itertools.cycle("|/-\\")
    while not stop_event.is_set():
        sys.stdout.write(f"\r{prefix} {next(spinner)}  (in Arbeit...)")
        sys.stdout.flush()
        time.sleep(0.1)

    # Spinner-Zeile löschen
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()


# ---------------------------------------------------------
# CLI Hauptfunktion
# ---------------------------------------------------------
def run_cli():
    parser = argparse.ArgumentParser(
        description=f"html2pdf - HTML → PDF Konverter (Version {__version__})"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")
    parser.add_argument("--silent", action="store_true")
    parser.add_argument("--log")
    args = parser.parse_args()

    logger = setup_logger(args.log)

    # Prüfen, ob wkhtmltopdf installiert ist
    ensure_wkhtmltopdf_or_raise()

    # Dateien sammeln
    files = resolve_input_path(args.input)
    if not files:
        raise SystemExit("Keine HTML-Dateien gefunden.")

    if len(files) > 1 and args.output and Path(args.output).suffix.lower() == ".pdf":
        raise SystemExit(
            "Bei mehreren Eingabedateien muss --output ein Verzeichnis sein, nicht eine einzelne PDF-Datei."
        )

    total = len(files)

    # ---------------------------------------------------------
    # Konvertierungsschleife
    # ---------------------------------------------------------
    for i, input_file in enumerate(files, start=1):
        output_file = build_output_path(input_file, args.output)

        # Spinner starten (nur wenn nicht silent)
        if not args.silent:
            prefix = f"[{i}/{total}] {input_file.name} → {output_file.name}"
            stop_event = threading.Event()
            spinner_thread = threading.Thread(
                target=start_spinner, args=(stop_event, prefix)
            )
            spinner_thread.start()

        # Konvertierung durchführen
        code, stdout, stderr = convert_single_html(input_file, output_file)

        # Spinner stoppen
        if not args.silent:
            stop_event.set()
            spinner_thread.join()

        # Ergebnis ausgeben
        if not args.silent:
            if code == 0:
                print(f"[{i}/{total}] {input_file.name} → {output_file.name}  ✔ Erfolgreich")
            else:
                print(f"[{i}/{total}] {input_file.name} → {output_file.name}  ✖ Fehler")
                logger.error(stderr)
