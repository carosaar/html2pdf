"""
runner.py – Zentrale Ablaufsteuerung für die CLI-Engine von html2pdf 0.5.0
"""

from pathlib import Path
import subprocess
import sys
import threading


from .parser import parse_arguments
from .input_resolver import resolve_input
from .output_resolver import resolve_output_directory, build_pdf_output_path
from .logger_engine import LogEngine


def run_wkhtmltopdf(input_file: Path, output_file: Path, silent: bool):
    """
    Startet wkhtmltopdf für eine einzelne Datei.
    Fortschrittsanzeige wird wie in früheren Versionen in EINER Zeile gehalten.
    """

    cmd = [
        "wkhtmltopdf",
        "--enable-local-file-access",   # WICHTIG: CSS/Bilder/JS erlauben
        str(input_file),
        str(output_file),
    ]

    try:
        if silent:
            # Keine Ausgabe → kein Deadlock
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True
            )
        else:
            # stderr im Textmodus für Fortschritt
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Fortschrittsanzeige in EINER Zeile
            def progress_reader(proc, infile, outfile):
                for line in proc.stderr:
                    line = line.strip()
                    if line:
                        sys.stdout.write(
                            f"\r{infile.name} → {outfile.name} | {line}   "
                        )
                        sys.stdout.flush()

            threading.Thread(
                target=progress_reader,
                args=(process, input_file, output_file),
                daemon=True
            ).start()

        # Prozess überwachen
        process.wait()

        # Rückgabe auswerten
        if process.returncode == 0:
            return True, ""
        else:
            return False, f"wkhtmltopdf Fehlercode {process.returncode}"

    except FileNotFoundError:
        return False, "wkhtmltopdf nicht gefunden"
    except Exception as e:
        return False, f"Ausnahme beim Aufruf von wkhtmltopdf: {e}"



def main():
    # ------------------------------------------------------------
    # 1. Argumente parsen
    # ------------------------------------------------------------
    args = parse_arguments()

    input_spec = args["input"]
    output_arg = args["output"]
    silent = args["silent"]
    logfile_name = args["logfile"]
    append = args["append"]

    # ------------------------------------------------------------
    # 2. Input-Dateien auflösen
    # ------------------------------------------------------------
    files = resolve_input(input_spec)

    if not files:
        # Keine Dateien gefunden
        if not silent:
            print(f"Keine Dateien gefunden für: {input_spec}")

        # Logging, falls aktiv
        if logfile_name is not None:
            # Wir brauchen trotzdem ein Output-Verzeichnis → nehmen das aktuelle
            out_dir = Path(".").resolve()
            logger = LogEngine(out_dir, logfile_name, append=append)
            logger.write_header(input_spec, out_dir)
            logger.write_entry("", "", f"Keine Dateien gefunden für: {input_spec}")
            logger.write_summary()

        # Kein Fehlercode, wie besprochen: ignorieren
        return

    # ------------------------------------------------------------
    # 3. Output-Verzeichnis bestimmen (anhand der ersten Datei)
    # ------------------------------------------------------------
    first_input = files[0]
    out_dir = resolve_output_directory(first_input, output_arg)

    # ------------------------------------------------------------
    # 4. Logging initialisieren (falls gewünscht)
    # ------------------------------------------------------------
    logger = None
    if logfile_name is not None:
        logger = LogEngine(out_dir, logfile_name, append=append)
        logger.write_header(input_spec, out_dir)

    ok_count = 0
    fail_count = 0

    # ------------------------------------------------------------
    # 5. Hauptschleife: Dateien konvertieren
    # ------------------------------------------------------------
    for input_file in files:
        pdf_path = build_pdf_output_path(input_file, out_dir)

        if not silent:
            print(f"Konvertiere: {input_file} -> {pdf_path}")

        success, error_text = run_wkhtmltopdf(input_file, pdf_path, silent=silent)

        if success:
            ok_count += 1
            status = "Erfolg"
            if not silent:
                print(f"Erfolg: {pdf_path}")
        else:
            fail_count += 1
            status = f"Fehler {error_text}"
            if not silent:
                print(f"Fehler bei {input_file}: {error_text}", file=sys.stderr)

        # Logging pro Datei
        if logger is not None:
            logger.write_entry(input_file.name, pdf_path.name, status)

    # ------------------------------------------------------------
    # 6. Zusammenfassung
    # ------------------------------------------------------------
    if not silent:
        print(f"{ok_count} Dateien erfolgreich, {fail_count} Dateien mit Fehlern")

    if logger is not None:
        logger.ok_count = ok_count
        logger.fail_count = fail_count
        logger.write_summary()