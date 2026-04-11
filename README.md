# HTML2PDF – HTML‑zu‑PDF Konverter (GUI & CLI)

Ein Python‑Tool zur Konvertierung von HTML‑Dateien in PDF mittels **wkhtmltopdf**.  
Unterstützt **GUI** (Tkinter) und **CLI** für automatisierte Workflows.

## ✨ Features

- GUI mit Dateiauswahl, Fortschrittsanzeige und Statusmeldungen  
- CLI für automatisierte Verarbeitung (Ordner oder Einzeldatei)  
- Automatische Erzeugung der PDF‑Dateinamen  
- Prüfung, ob `wkhtmltopdf` installiert ist  
- Logging‑Unterstützung  
- Saubere, modulare Projektstruktur (`src/`‑Layout)

## 📦 Installation

Voraussetzung: Python 3.10+

```
pip install .
```

Start der GUI:

```
html2pdf
```

CLI‑Modus:

```
html2pdf --input <pfad> [--output <ordner>] [--silent] [--log <datei>]
```

Beispiele:

```
html2pdf --input C:\webseite\index.html
html2pdf --input C:\webseiten\ --output C:\pdfs\
```

## 🔧 Voraussetzungen

- Installiertes `wkhtmltopdf`  
  Download: https://wkhtmltopdf.org/downloads.html  
- Windows, Linux oder macOS

## 📁 Projektstruktur

```
src/html2pdf/
    main.py
    core/
    gui/
    cli/
    docs/
```

## 📄 Lizenz

Dieses Projekt steht unter der **MIT‑Lizenz**.  
Siehe Datei `LICENSE` für Details.

