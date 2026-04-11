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
    """
    if output_folder:
        out_dir = Path(output_folder)
    else:
        out_dir = input_file.parent

    return out_dir / (input_file.stem + ".pdf")
