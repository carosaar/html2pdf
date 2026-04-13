"""
CLI-Frontend für automatisierte Verarbeitung.
"""

import argparse
import threading
import sys
import time
from pathlib import Path

from html2pdf.core.file_utils import resolve_input_path, build_output_path
from html2pdf.core.converter import start_wkhtmltopdf, run_and_wait
from html2pdf.core.logger import setup_logger
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__


def run_cli():
    parser = argparse.ArgumentParser(
        description=f"html2pdf - HTML → PDF Konverter (Version {__version__})"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")
    parser.add_argument("--silent", action="store_true")
    parser.add_argument("--log")
    args = parser.parse_args()

    # Logdatei automatisch bestimmen
    if args.log:
        log_path = Path(args.log)
    else:
        input_path = Path(args.input)
        base = input_path.stem
        log_path = input_path.with_name(f"{base}_log.txt")

    # Logger initialisieren – aber nur wenn nicht silent
    if args.silent:
        logger = None
    else:
        # Logdatei neu schreiben, nicht anhängen
        if log_path.exists():
            log_path.unlink()

        logger = setup_logger(str(log_path))

    ensure_wkhtmltopdf_or_raise()

    files = resolve_input_path(args.input)
    if not files:
        raise SystemExit("Keine HTML-Dateien gefunden.")

    if len(files) > 1 and args.output and Path(args.output).suffix.lower() == ".pdf":
        raise SystemExit(
            "Bei mehreren Eingabedateien muss --output ein Verzeichnis sein."
        )

    total = len(files)

    for i, input_file in enumerate(files, start=1):
        output_file = build_output_path(input_file, args.output)

        # Logging: Start der Verarbeitung
        if logger:
            logger.info(f"Verarbeite: {input_file.resolve()}")

        # Silent-Mode: kein stderr → kein Deadlock → keine Ausgabe
        process = start_wkhtmltopdf(
            input_file,
            output_file,
            capture_stderr=not args.silent
        )

        # Fortschritt nur anzeigen, wenn nicht silent
        if not args.silent and process.stderr is not None:
            def read_stderr(proc, index, total_files, in_file, out_file):
                for line in proc.stderr:
                    line = line.strip()
                    if line:
                        sys.stdout.write(
                            f"\r[{index}/{total_files}] {in_file.name} → {out_file.name} | {line}   "
                        )
                        sys.stdout.flush()

            threading.Thread(
                target=read_stderr,
                args=(process, i, total, input_file, output_file),
                daemon=True,
            ).start()

        # Prozess überwachen
        while process.poll() is None:
            time.sleep(0.1)

        code, stdout, stderr = run_and_wait(process)

        # Logging: Erfolg oder Fehler
        if code == 0:
            if logger:
                logger.info(f"Erstellt: {output_file.resolve()}")
        else:
            if logger:
                logger.error(f"Fehler bei {input_file.resolve()}: {stderr or 'Unbekannter Fehler'}")

        # Trennzeile
        if logger:
            logger.info("---")

        # Ergebnis nur im nicht-silent-Modus ausgeben
        if not args.silent:
            sys.stdout.write("\r" + " " * 120 + "\r")
            sys.stdout.flush()

            if code == 0:
                print(f"[{i}/{total}] {input_file.name} → {output_file.name}  ✔ Erfolgreich")
            else:
                print(f"[{i}/{total}] {input_file.name} → {output_file.name}  ✖ Fehler")