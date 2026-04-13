"""
output_resolver.py – Auflösung des Output-Verzeichnisses und
Generierung der PDF-Ausgabepfade für html2pdf 0.5.0
"""

from pathlib import Path


def resolve_output_directory(input_path: Path, output_arg: str | None) -> Path:
    """
    Bestimmt das Output-Verzeichnis.

    Regeln:
    - Wenn --output fehlt → Verzeichnis der Input-Datei verwenden
    - Wenn --output angegeben ist → muss ein Verzeichnis sein
    - Verzeichnis wird automatisch erstellt
    """

    # Fall 1: Kein Output angegeben → Input-Verzeichnis
    if output_arg is None:
        out_dir = input_path.parent

    else:
        out_dir = Path(output_arg)

    # Output muss ein Verzeichnis sein
    # Falls es nicht existiert → automatisch erstellen
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise SystemExit(f"Fehler: Output-Verzeichnis konnte nicht erstellt werden: {e}")

    return out_dir


def build_pdf_output_path(input_file: Path, output_dir: Path) -> Path:
    """
    Erzeugt den vollständigen Pfad zur PDF-Ausgabedatei.

    Regeln:
    - PDF-Name = Basename der HTML-Datei + '.pdf'
    - Existierende Dateien werden überschrieben (keine Rückfrage)
    """

    base = input_file.stem
    pdf_name = base + ".pdf"
    return output_dir / pdf_name