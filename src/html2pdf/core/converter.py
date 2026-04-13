"""
Kernlogik für die HTML→PDF-Konvertierung (Version 0.3.x).
Mit sofort abbrechbaren Prozessen und optionaler stderr-Erfassung.
"""

import subprocess
import signal
from pathlib import Path
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise


def start_wkhtmltopdf(input_file: Path, output_file: Path, capture_stderr=True):
    wkhtml = ensure_wkhtmltopdf_or_raise()

    cmd = [
        wkhtml,
        "--enable-local-file-access",
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