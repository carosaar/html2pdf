# 📄 **README.md**

html2pdf  Version 0.5.2
Ein einfacher HTML‑zu‑PDF‑Konverter mit GUI und CLI, basierend auf `wkhtmltopdf`.

Das Projekt bietet:
- eine komfortable **GUI** (Drag & Drop, Batch‑Verarbeitung)
- eine **CLI** für automatisierte Konvertierungen
- eine portable **Windows‑EXE** (PyInstaller)
- eingebettete `wkhtmltopdf`‑Binaries für Offline‑Nutzung

## Das Benutzerhandbuch [findet sich unter src/html2pdf/docs](src/html2pdf/docs/HANDBUCH.md)

---

## 📦 Installation nach dem Klonen

### 1. Repository klonen
```bash
git clone https://github.com/carosaar/html2pdf.git
cd html2pdf
```

### 2. Paket lokal installieren
Das Projekt verwendet ein klassisches `src/`‑Layout.  
Die Paketinstallation erfolgt mit:

```bash
pip install .
```

Damit wird das Paket in die Python‑Umgebung eingebunden und die Startbefehle erzeugt.

---

## 🚀 Starten der Anwendung

### GUI starten
```bash
html2pdf
```

oder alternativ:

```bash
python -m html2pdf
```

### CLI starten
```bash
html2pdf --input input.html --output out/
```

Weitere CLI‑Optionen:
```bash
html2pdf --help
```

---

## 📁 Projektstruktur

```
src/
    html2pdf/
        __init__.py
        __main__.py
        version.py
        core/
            converter.py
            file_utils.py
            wkhtmltopdf_check.py
        gui/
            gui_app.py
        cli/
            cli_app.py
        assets/
            html2pdf.ico
        bin/
            wkhtmltopdf.exe
            libwkhtmltox.dll
```

- **GUI‑Startpunkt:** `gui/gui_app.py`  
- **CLI‑Startpunkt:** `cli/cli_app.py`  
- **Python‑Startpunkt:** `__main__.py`  
- **wkhtmltopdf‑Binaries:** `bin/`  

---

## 🛠 PyInstaller‑Build

Das Projekt enthält eine funktionierende `html2pdf.spec`.  
Der Build erfolgt mit:

```bash
pyinstaller html2pdf.spec --noconfirm
```

Die fertige EXE liegt anschließend unter:

```
dist/html2pdf.exe
```

Die EXE enthält:
- GUI
- eingebettete wkhtmltopdf‑Binaries
- Icon
- alle benötigten Module

---


## 📜 MIT Lizenz
Dieses Projekt verwendet die Lizenz aus der Datei `LICENSE`.  
Die eingebetteten wkhtmltopdf‑Binaries stehen unter [LGPL](LISENSES/wkhtmltopdf-LGPL-3.0.txt)

---

## 🤝 Mitwirken
Pull Requests und Verbesserungen sind willkommen.

## Autor
(c) 2026 by Dieter Eckstein
