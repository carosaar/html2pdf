"""
Einfaches Logging-Modul.
"""

import logging
from html2pdf.version import __version__

_logger_initialized = False

def setup_logger(logfile=None):
    global _logger_initialized

    logger = logging.getLogger("html2pdf")
    logger.setLevel(logging.INFO)

    # Verhindert doppelte Handler bei mehrfachen Aufrufen
    if not _logger_initialized:

        # Nur Datei-Logging, niemals stdout
        if logfile:
            handler = logging.FileHandler(logfile, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # Startmeldung nur ins Logfile
            logger.info(f"Starte html2pdf Version {__version__}")

        # Wenn kein logfile → KEIN Handler, KEINE Ausgabe
        else:
            logger.handlers.clear()

        _logger_initialized = True

    return logger