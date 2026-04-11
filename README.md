# 📘 **README.md (Version 0.2.1)**

# html2pdf  
GUI- und CLI‑Tool zur HTML‑zu‑PDF‑Konvertierung mit wkhtmltopdf

**html2pdf** ist ein leichtgewichtiges, schnelles und plattformfreundliches Werkzeug zur Konvertierung von statischen HTML‑Dateien in PDF‑Dokumente.  
Es bietet sowohl eine **grafische Benutzeroberfläche (GUI)** als auch eine **Kommandozeilen‑Schnittstelle (CLI)** und nutzt intern das bewährte Tool **wkhtmltopdf**.

---

## 🚀 Funktionen

### ✔ GUI‑Funktionen (Version 0.2.1)

- Mehrfachauswahl von HTML‑Dateien  
- Tabellenansicht mit:
  - HTML‑Datei  
  - HTML‑Ordner (relativ zum Arbeitsordner)  
  - PDF‑Datei  
  - PDF‑Ordner  
  - Status (Bereit, In Arbeit…, Fertig ✔, Fehler, Abgebrochen)  
- Drag & Drop Unterstützung (falls `tkinterdnd2` installiert ist)  
- Ausgabeordner wählen  
- Fortschrittsanzeige mit Animation  
- Doppelklick zum Entfernen einzelner Einträge  
- **🗑️ Liste leeren**  
- **⛔ Abbrechen** einer laufenden Konvertierung (mit akustischem Signal + Dialog)  
- **Beenden‑Button**  
- GUI bleibt auch bei sehr großen Dateimengen (10.000+) reaktionsfähig  

---

## 🖥️ CLI‑Funktionen

Die CLI ist ideal für Automatisierung, Skripte oder Batch‑Verarbeitung.

Beispiel:

```bash
html2pdf input.html output.pdf
```

Weitere Optionen:

```bash
html2pdf --help
```

---

## 📦 Installation

### 1. Python installieren  

Erforderlich: **Python 3.10 oder höher**

### 2. Repository klonen

```bash
git clone https://github.com/carosaar/html2pdf.git
cd html2pdf
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Paket installieren (lokal)

```bash
pip install .
```

### 5. GUI starten

```bash
python -m html2pdf.gui
```

oder (falls als Script installiert):

```bash
html2pdf
```

---

## 🛠️ Voraussetzung: wkhtmltopdf

Dieses Projekt nutzt **wkhtmltopdf.exe** zur PDF‑Erzeugung.

Download:  
`https://wkhtmltopdf.org/downloads.html` [(wkhtmltopdf.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwkhtmltopdf.org%2Fdownloads.html")

Nach der Installation muss `wkhtmltopdf` im **PATH** liegen.

---

## 📁 Projektstruktur

```text
html2pdf/
 ├── core/
 │    ├── converter.py          # Aufruf von wkhtmltopdf
 │    ├── file_utils.py         # Pfadberechnung
 │    ├── wkhtmltopdf_check.py  # Prüfung der Installation
 │
 ├── gui/
 │    └── gui_app.py            # Tkinter GUI (Version 0.2.1)
 │
 ├── cli/
 │    └── main.py               # CLI-Einstiegspunkt
 │
 ├── assets/
 │    └── html2pdf.ico          # App-Icon
 │
 ├── version.py                 
 └── ...
```

---

## 🔧 Entwicklung

### Projekt bauen

```bash
python -m build
```

### Tests (optional)

```bash
pytest
```

---

## 📄 Lizenz

Dieses Projekt steht unter der **MIT‑Lizenz**.  
Siehe Datei `LICENSE`.

---

## 🤝 Mitwirken

Pull Requests sind willkommen!  
Bitte achte auf:

- klare Commit‑Nachrichten  
- saubere Struktur  
- funktionierende GUI/CLI  
- reproduzierbare Fehlerbeschreibungen  

---

## Autor

(c) 2026 Dieter Eckstein

## ⭐ Feedback

Wenn dir das Tool gefällt, freue ich mich über ein ⭐ auf GitHub!
