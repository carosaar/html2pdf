"""
Kernlogik für die HTML→PDF-Konvertierung (Version 0.3.x).
Mit sofort abbrechbaren Prozessen und optionaler stderr-Erfassung.
    # ------------------------------------------------------------
    # wkhtmltopdf-Konfiguration
    # ------------------------------------------------------------
    # Wir erzwingen hier das Seitenformat A4, da wkhtmltopdf CSS-Angaben
    # wie @page { size: A4 } ignoriert und ausschließlich Kommandozeilen-
    # Parameter für die Seitengröße akzeptiert.
    #
    # --page-size A4
    #     Setzt das physische Seitenformat auf A4 (210 × 297 mm).
    #
    # --orientation Portrait
    #     Standardausrichtung für OFB-Ausgaben. Landscape wäre optional.
    #
    # --encoding utf-8
    #     Stellt sicher, dass Umlaute und Sonderzeichen korrekt gerendert
    #     werden. Ohne diese Option kann wkhtmltopdf Zeichen falsch
    #     interpretieren.
    #
    # --enable-local-file-access
    #     Erlaubt das Laden lokaler Ressourcen (CSS, Bilder, Icons).
    #     Ohne diese Option würden Bilder wie bir1.gif oder dea1.gif
    #     nicht angezeigt.
    #
    # Diese Parameter sind zwingend notwendig, da wkhtmltopdf weder
    # HTML- noch CSS-Angaben für das Seitenformat zuverlässig auswertet.
    # ------------------------------------------------------------
"""

import subprocess
import signal
from pathlib import Path
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise


def start_wkhtmltopdf(input_file: Path, output_file: Path, capture_stderr=True):
    wkhtml = ensure_wkhtmltopdf_or_raise()

    # ------------------------------------------------------------
    # wkhtmltopdf-Konfiguration
    # (Kommentarblock siehe oben)
    # ------------------------------------------------------------
    cmd = [
        wkhtml,
        "--enable-local-file-access",
        "--page-size", "A4",
        "--orientation", "Portrait",
        "--encoding", "utf-8",
        str(input_file),
        str(output_file)
    ]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE if capture_stderr else subprocess.DEVNULL,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    return process


def run_and_wait(process):
    process.wait()
    return process.returncode, "", ""