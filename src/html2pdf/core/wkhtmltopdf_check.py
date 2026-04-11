"""
Prüft, ob wkhtmltopdf installiert ist.
"""

import shutil

def find_wkhtmltopdf():
    return shutil.which("wkhtmltopdf")

def ensure_wkhtmltopdf_or_raise():
    path = find_wkhtmltopdf()
    if path is None:
        raise RuntimeError(
            "wkhtmltopdf wurde nicht gefunden.\n"
            "Bitte installieren Sie wkhtmltopdf:\n"
            "https://wkhtmltopdf.org/downloads.html\n\n"
            "Stellen Sie sicher, dass es im PATH liegt."
        )
    return path
