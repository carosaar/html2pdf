"""
Hilfsfunktionen für Datei- und Ordnerverarbeitung.
"""

from pathlib import Path

def resolve_input_path(path_str):
    """
    Unterscheidet zuverlässig zwischen Datei und Ordner.
    Gibt eine Liste von HTML-Dateien zurück.
    """
    p = Path(path_str)

    if not p.exists():
        raise FileNotFoundError(f"Pfad existiert nicht: {p}")

    if p.is_file():
        return [p]

    if p.is_dir():
        return list(p.glob("*.html"))

    raise ValueError("Pfad ist weder Datei noch Ordner.")

def build_output_path(input_file, output_folder=None):
    """
    Erzeugt den PDF-Ausgabepfad aus der HTML-Datei.

    Wenn `output_folder` eine vorhandene oder neue PDF-Datei ist und nur eine
    einzelne HTML-Datei verarbeitet wird, wird dieser Dateiname direkt verwendet.
    Ansonsten wird davon ausgegangen, dass `output_folder` ein Verzeichnis ist.
    """
    if output_folder:
        out_path = Path(output_folder)

        if out_path.suffix.lower() == ".pdf":
            return out_path

        return out_path / (input_file.stem + ".pdf")

    return input_file.parent / (input_file.stem + ".pdf")
