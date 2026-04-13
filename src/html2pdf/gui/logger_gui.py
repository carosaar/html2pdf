"""
logger_gui.py – Logging-System für die GUI von html2pdf 0.5.0

Funktionen:
- Header schreiben
- Dateien gruppieren nach Eingabe- und Ausgabepfaden
- CLI-kompatible Ergebniszeilen schreiben
- Zusammenfassung am Ende
- Immer überschreiben
"""

from pathlib import Path
from datetime import datetime
from collections import defaultdict


class GuiLogger:
    def __init__(self, logfile_path: Path):
        """
        logfile_path: Vollständiger Pfad zur Logdatei.
        Datei wird IMMER überschrieben.
        """
        self.logfile_path = logfile_path

        # Struktur:
        # { (input_dir, output_dir): [ (input_file, output_file, status) ] }
        self.entries = defaultdict(list)

        self.ok_count = 0
        self.fail_count = 0

    # ------------------------------------------------------------
    # Öffentliche API
    # ------------------------------------------------------------

    def add_entry(self, input_path: Path, output_path: Path, status: str):
        """
        Fügt einen Logeintrag hinzu.
        input_path: vollständiger Pfad zur Eingabedatei
        output_path: vollständiger Pfad zur Ausgabedatei
        status: "Erfolg" oder "Fehler <Text>"
        """

        input_dir = str(input_path.parent.resolve())
        output_dir = str(output_path.parent.resolve())

        self.entries[(input_dir, output_dir)].append(
            (input_path.name, output_path.name, status)
        )

        if status.startswith("Erfolg"):
            self.ok_count += 1
        else:
            self.fail_count += 1

    def write_log(self):
        """
        Schreibt die vollständige Logdatei.
        """

        try:
            with self.logfile_path.open("w", encoding="utf-8") as f:
                self._write_header(f)
                self._write_grouped_entries(f)
                self._write_summary(f)

        except Exception as e:
            raise SystemExit(f"Fehler beim Schreiben der GUI-Logdatei: {e}")

    # ------------------------------------------------------------
    # Interne Hilfsfunktionen
    # ------------------------------------------------------------

    def _write_header(self, f):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        header = (
            "##############################\n"
            f"# html2pdf Konvertierung vom {timestamp}\n"
            f"# Logdatei: {self.logfile_path}\n"
            "##############################\n\n"
        )
        f.write(header)

    def _write_grouped_entries(self, f):
        """
        Sortiert und schreibt:
        1. Eingabepfade alphabetisch
        2. Ausgabepfade alphabetisch
        3. Dateien alphabetisch
        """

        # Sortierung der Gruppen
        for (input_dir, output_dir) in sorted(self.entries.keys()):
            f.write(f"# Eingabepfad: {input_dir}\n")
            f.write(f"# Ausgabepfad: {output_dir}\n")

            # Dateien sortieren
            file_entries = sorted(self.entries[(input_dir, output_dir)],
                                  key=lambda x: x[0])  # sort by input filename

            for input_name, output_name, status in file_entries:
                f.write(f"{input_name};{output_name};{status}\n")

            f.write("\n")

    def _write_summary(self, f):
        summary = (
            f"{self.ok_count} Dateien erfolgreich\n"
            f"{self.fail_count} Dateien mit Fehlern\n"
        )
        f.write(summary)