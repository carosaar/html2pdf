"""
input_resolver.py – Auflösung von Input-Pfaden, Masken und Endungen
für html2pdf 0.5.0
"""

from pathlib import Path
import glob


def _ensure_html_extension(pattern: str) -> str:
    """
    Ergänzt .html, wenn der Benutzer keine Endung angegeben hat.
    Beispiele:
        "*"          -> "*.html"
        "bericht"    -> "bericht.html"
        "datei*"     -> "datei*.html"
        "*.htm?"     -> "*.htm?"  (bereits gültige Endung)
    """
    p = pattern.strip()

    # Wenn bereits eine Endung vorhanden ist → nichts tun
    if "." in Path(p).name:
        return p

    # Keine Endung → .html ergänzen
    return p + ".html"


def _resolve_mask(pattern: str) -> list[Path]:
    """
    Löst Masken wie *.html oder datei*.htm? auf.
    Gibt eine Liste von Path-Objekten zurück.
    """
    # glob.glob liefert Strings → in Path umwandeln
    return [Path(p) for p in glob.glob(pattern)]


def resolve_input(input_value: str) -> list[Path]:
    """
    Hauptfunktion:
    - erkennt Masken
    - ergänzt Endungen
    - löst Verzeichnisse auf
    - sortiert alphabetisch
    - gibt eine Liste von Path-Objekten zurück
    """

    raw = input_value.strip()
    p = Path(raw)

    # --- Fall 1: Verzeichnis ---
    if p.is_dir():
        # Alle HTML-Dateien im Verzeichnis
        files = sorted(p.glob("*.html"))
        return files

    # --- Fall 2: Einzeldatei ---
    if p.is_file():
        return [p]

    # --- Fall 3: Maske ---
    # Masken enthalten * oder ?
    if "*" in raw or "?" in raw:
        pattern = _ensure_html_extension(raw)
        files = _resolve_mask(pattern)
        return sorted(files)

    # --- Fall 4: Einzeldatei ohne Endung ---
    # z. B. "bericht" → "bericht.html"
    pattern = _ensure_html_extension(raw)
    files = _resolve_mask(pattern)
    return sorted(files)