# 📘 **README.md (Version 0.4.0)**

# html2pdf  
GUI‑ und CLI‑Tool zur HTML‑zu‑PDF‑Konvertierung mit **eingebetteter wkhtmltopdf‑Engine**

**html2pdf** ist ein leichtgewichtiges, schnelles und plattformfreundliches Werkzeug zur Konvertierung von statischen HTML‑Dateien in PDF‑Dokumente.  
Es bietet sowohl eine **grafische Benutzeroberfläche (GUI)** als auch eine **Kommandozeilen‑Schnittstelle (CLI)** und enthält ab Version **0.4.0** eine **portable Version von wkhtmltopdf**, sodass **keine Installation** von wkhtmltopdf mehr erforderlich ist.

---

## 🚀 Funktionen

### ✔ GUI‑Funktionen (Version 0.4.0)

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
- **⛔ Abbrechen** einer laufenden Konvertierung  
  - der laufende `wkhtmltopdf`‑Prozess wird sofort beendet  
- **Beenden‑Button wird während der Konvertierung deaktiviert**  
- GUI bleibt auch bei sehr großen Dateimengen (10.000+) reaktionsfähig  
- Automatische Nutzung der eingebetteten wkhtmltopdf‑Engine  

---

## 🖥️ CLI‑Funktionen

Die CLI ist ideal für Automatisierung, Skripte oder Batch‑Verarbeitung.

Beispiel:

```bash
html2pdf --input input.html --output output.pdf --log logger.txt
```

Weitere Optionen:

```bash
html2pdf --help
```

>html2pdf – HTML → PDF Konverter (Version 0.4.0)

options:
  -h, --help       show this help message and exit  
  --input INPUT  
  --output OUTPUT  
  --silent  
  --log LOG  

---

## 🛠️ Eingebettete wkhtmltopdf‑Engine (ab Version 0.4.0)

html2pdf enthält eine **portable Version von wkhtmltopdf**  
(`wkhtmltopdf.exe` + `libwkhtmltox.dll`) im Ordner:

```
html2pdf/bin/
```

Dadurch funktioniert html2pdf:

- **ohne Installation** von wkhtmltopdf  
- **ohne PATH‑Eintrag**  
- **ohne Administratorrechte**  
- **vollständig portabel**  

Falls die interne Version fehlt, versucht html2pdf automatisch, eine Systeminstallation zu verwenden.

---

## 📦 Installation (Python‑Version)

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

## 📁 Projektstruktur

```text
html2pdf/
 ├── core/
 │    ├── converter.py          # Aufruf der eingebetteten wkhtmltopdf-Engine
 │    ├── file_utils.py         # Pfadberechnung
 │    ├── wkhtmltopdf_check.py  # Erkennung der internen/externen Engine
 │
 ├── gui/
 │    └── gui_app.py            # Tkinter GUI
 │
 ├── cli/
 │    └── main.py               # CLI-Einstiegspunkt
 │
 ├── assets/
 │    └── html2pdf.ico          # App-Icon
 │
 ├── bin/                       # Eingebettete wkhtmltopdf-Engine (NEU ab 0.4.0)
 │    ├── wkhtmltopdf.exe
 │    └── libwkhtmltox.dll
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

html2pdf steht unter der MIT‑Lizenz (siehe LICENSE).

### Nutzung von wkhtmltopdf

html2pdf verwendet die Software **wkhtmltopdf**, die unter der  
GNU Lesser General Public License Version 3 (LGPL‑3.0) veröffentlicht wird.

Ab Version **0.4.0** wird eine **unveränderte portable Version** von wkhtmltopdf  
(`wkhtmltopdf.exe` + `libwkhtmltox.dll`) direkt mitgeliefert.

Gemäß LGPL‑3.0 ist dies zulässig, solange:

- die LGPL‑Lizenz beigefügt wird,  
- ein Hinweis auf die Nutzung erfolgt,  
- Änderungen an wkhtmltopdf (falls vorhanden) offengelegt werden (Es sind keine Änderungen vorgenommen worden).  

html2pdf nimmt **keine Änderungen** an wkhtmltopdf vor.

Die vollständigen Lizenztexte befinden sich in:

- `LICENSE` (MIT‑Lizenz für html2pdf)  
- `LICENSES/wkhtmltopdf-LGPL-3.0.txt` (LGPL‑3.0 für wkhtmltopdf)  

---

## 🤝 Mitwirken

Pull Requests sind willkommen!  
Bitte achte auf:

- klare Commit‑Nachrichten  
- saubere Struktur  
- funktionierende GUI/CLI  
- reproduzierbare Fehlerbeschreibungen  

---

## 👤 Autor

(c) 2026 Dieter Eckstein

---

## ⭐ Feedback

Wenn dir das Tool gefällt, freue ich mich über ein ⭐ auf GitHub!
