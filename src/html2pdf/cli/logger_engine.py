"""
logger_engine.py – Logging-System für html2pdf 0.5.0

Funktionen:
- Kopfbereich schreiben
- Ergebniszeilen schreiben
- Zusammenfassung schreiben
- Append- oder Overwrite-Modus
- Endungsergänzung (.txt)
- Logdatei immer im Output-Verzeichnis
"""

from pathlib import Path
from datetime import datetime


class LogEngine:
    def __init__(self, output_dir: Path, logfile_name: str, append: bool = False):
        """
        output_dir: Verzeichnis, in dem die Logdatei gespeichert wird
        logfile_name: Name der Logdatei (Endung wird ergänzt, falls fehlt)
        append: True = an bestehende Datei anhängen, False = überschreiben
        """

        self.output_dir = output_dir
        self.logfile_path = self._resolve_logfile_path(logfile_name)
        self.append = append

        # interner Zähler für Zusammenfassung
        self.ok_count = 0
        self.fail_count = 0

    # ------------------------------------------------------------
    # Hilfsfunktionen
    # ------------------------------------------------------------

    def _ensure_txt_extension(self, name: str) -> str:
        """
        Ergänzt .txt, wenn der Benutzer keine Endung angegeben hat.
        """
        if "." not in Path(name).name:
            return name + ".txt"
        return name

    def _resolve_logfile_path(self, logfile_name: str) -> Path:
        """
        Erzeugt den vollständigen Pfad zur Logdatei im Output-Verzeichnis.
        """
        name = self._ensure_txt_extension(logfile_name)
        return self.output_dir / name

    def _write(self, text: str):
        """
        Schreibt Text in die Logdatei.
        """
        mode = "a" if self.append else "w"
        try:
            with self.logfile_path.open(mode, encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            raise SystemExit(f"Fehler beim Schreiben der Logdatei: {e}")

        # Nach dem ersten Schreiben immer in Append-Modus wechseln
        self.append = True

    # ------------------------------------------------------------
    # Öffentliche API
    # ------------------------------------------------------------

    def write_header(self, input_mask: str, output_dir: Path):
        """
        Schreibt den Kopfbereich der Logdatei.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        header = (
            "##############################\n"
            f"# html2pdf Konvertierung vom {timestamp}\n"
            f"# Eingabe: {input_mask}\n"
            f"# Ausgabe: {output_dir}\n"
            f"# Logdatei: {self.logfile_path}\n"
            "##############################\n"
        )

        self._write(header)

    def write_entry(self, input_name: str, output_name: str, status: str):
        """
        Schreibt eine Ergebniszeile:
        input.html;output.pdf;Erfolg
        input.html;output.pdf;Fehler <Text>
        """

        line = f"{input_name};{output_name};{status}\n"
        self._write(line)

        # Zähler aktualisieren
        if status.startswith("Erfolg"):
            self.ok_count += 1
        else:
            self.fail_count += 1

    def write_summary(self):
        """
        Schreibt die Zusammenfassung am Ende der Logdatei.
        """
        summary = (
            f"{self.ok_count} Dateien erfolgreich\n"
            f"{self.fail_count} Dateien mit Fehlern\n"
        )
        self._write(summary)