"""
Kernlogik für die HTML→PDF-Konvertierung (Version 0.3.0).
Mit sofort abbrechbaren Prozessen.
"""

import subprocess
from pathlib import Path
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise


import subprocess
import signal

def start_wkhtmltopdf(input_file: Path, output_file: Path):
    wkhtml = ensure_wkhtmltopdf_or_raise()

    cmd = [
        wkhtml,
        "--enable-local-file-access",
        str(input_file),
        str(output_file)
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # <<< WICHTIG
    )

    return process

def run_and_wait(process):
    """
    Wartet auf den Prozess und gibt (returncode, stdout, stderr) zurück.
    """
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr