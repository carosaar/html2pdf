"""
Kernlogik für die HTML→PDF-Konvertierung.
"""

import subprocess
from pathlib import Path
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__

def convert_single_html(input_file: Path, output_file: Path):
    """
    Führt die Konvertierung einer einzelnen Datei durch.
    """
    wkhtml = ensure_wkhtmltopdf_or_raise()

    cmd = [
        wkhtml,
        "--enable-local-file-access",
        str(input_file),
        str(output_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode, result.stdout, result.stderr


def convert_multiple(files, output_folder=None, progress_callback=None):
    """
    Konvertiert mehrere Dateien nacheinander.
    progress_callback(index, total, input_file, output_file)
    """
    total = len(files)

    for index, input_file in enumerate(files, start=1):
        output_file = Path(output_folder) / (input_file.stem + ".pdf") \
            if output_folder else input_file.with_suffix(".pdf")

        if progress_callback:
            progress_callback(index, total, input_file, output_file)

        yield convert_single_html(input_file, output_file)
