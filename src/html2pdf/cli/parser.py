"""
parser.py – Argumentparser für html2pdf 0.5.0
"""

import argparse
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(
        description="html2pdf – HTML → PDF Konverter (CLI, Version 0.5.0)"
    )

    # Pflichtparameter: INPUT
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Eingabedatei, Verzeichnis oder Maske (z.B. *.html)"
    )

    # Optional: OUTPUT-Verzeichnis
    parser.add_argument(
        "-o", "--output",
        help="Ausgabeverzeichnis (optional, wird automatisch erstellt)"
    )

    # Silent-Modus
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="Unterdrückt alle Konsolenausgaben"
    )

    # Logging: -l und -la schließen sich gegenseitig aus
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-l", "--log",
        metavar="LOGDATEI",
        help="Logdateiname (wird im Output-Verzeichnis gespeichert)"
    )

    group.add_argument(
        "-la", "--logappend",
        metavar="LOGDATEI",
        help="Logdateiname (Anhängen an bestehende Datei)"
    )

    return parser


def parse_arguments():
    parser = build_parser()
    args = parser.parse_args()

    # --- Validierung ---

    # INPUT ist Pflicht → bereits durch argparse gesichert

    # OUTPUT ist optional → keine Validierung hier, erst im Resolver

    # Logging: Wenn -l oder -la gesetzt sind, muss ein Dateiname angegeben sein
    logfile = None
    append = False

    if args.log:
        if not args.log.strip():
            raise SystemExit("Fehler: Für --log muss ein Dateiname angegeben werden.")
        logfile = args.log.strip()
        append = False

    if args.logappend:
        if not args.logappend.strip():
            raise SystemExit("Fehler: Für --logappend muss ein Dateiname angegeben werden.")
        logfile = args.logappend.strip()
        append = True

    # Rückgabe eines klaren Parameterobjekts
    return {
        "input": args.input,
        "output": args.output,
        "silent": args.silent,
        "logfile": logfile,   # None oder Dateiname
        "append": append      # True = anhängen, False = überschreiben
    }