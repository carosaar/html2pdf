# 🟦 **README** html2pdf – Version 0.4.1
GUI‑ und CLI‑Tool zur HTML‑zu‑PDF‑Konvertierung mit eingebetteter wkhtmltopdf‑Engine

**html2pdf** ist ein schnelles, portables Werkzeug zur Konvertierung von HTML‑Dateien in PDF‑Dokumente.  
Es bietet sowohl eine **grafische Benutzeroberfläche (GUI)** als auch eine **Kommandozeilen‑Schnittstelle (CLI)** und enthält eine **portable Version von wkhtmltopdf**, sodass **keine Installation** erforderlich ist.

---

## 🚀 Neuerungen in Version 0.4.1

### ✔ Deadlock‑Fix für große HTML‑Dateien
- wkhtmltopdf erzeugt umfangreiche stderr‑Ausgaben  
- diese führten bei früheren Versionen zu Hängern  
- 0.4.1 nutzt nun:
  - **Live‑Auslesen von stderr** (GUI & nicht‑silent CLI)  
  - **DEVNULL‑Umleitung im Silent‑Mode**  
- Ergebnis: **keine Hänger mehr**, auch bei sehr großen Dateien

### ✔ Silent‑Mode vollständig korrigiert
- keine Fortschrittsmeldungen  
- keine Logger‑Ausgaben  
- keine Startmeldung  
- keine versteckten stderr‑Flushes  
- absolut geräuschlos

### ✔ Logging überarbeitet
- Logdatei wird **neu geschrieben**, nicht angehängt  
- Automatische Logdatei: `<basename>_log.txt`  
- Pro Datei wird protokolliert:
  - Eingabedatei (vollständiger Pfad)  
  - Ausgabedatei (vollständiger Pfad)  
  - Fehler (falls vorhanden)  
  - Trennzeile `---`  

### ✔ GUI: Live‑Fortschrittsanzeige
- stderr‑Ausgabe von wkhtmltopdf wird live in der Statuszeile angezeigt  
- Abbruchfunktion bleibt sofort wirksam  
- große Dateien funktionieren zuverlässig

---

## 🖥️ GUI‑Funktionen

- Mehrfachauswahl von HTML‑Dateien  
- Tabellenansicht mit Pfaden und Status  
- Drag & Drop Unterstützung  
- Ausgabeordner wählen  
- Fortschrittsanzeige + Live‑Status aus wkhtmltopdf  
- Abbrechen‑Button (sofort wirksam)  
- Doppelklick zum Entfernen  
- Liste leeren  
- GUI bleibt auch bei sehr großen Dateimengen reaktionsfähig  
- Nutzung der eingebetteten wkhtmltopdf‑Engine  

Starten:

```bash
html2pdf
```

oder:

```bash
python -m html2pdf.gui
```

---

## 🖥️ CLI‑Funktionen

Beispiel:

```bash
html2pdf --input input.html --output out/ --log
```

Optionen:

```
--input <datei/ordner>
--output <datei/ordner>
--silent
--log <optional: logfile>
```

### Logging (neu in 0.4.1)

- Standard: `<basename>_log.txt`  
- Inhalt pro Datei:
  ```
  Verarbeite: C:\Pfad\input.html
  Erstellt:   C:\Pfad\output.pdf
  ---
  ```

Silent‑Mode:

- keine Ausgabe  
- kein Logging  
- kein Fortschritt  

---

## 🛠️ Eingebettete wkhtmltopdf‑Engine

html2pdf enthält eine portable Version von wkhtmltopdf im Ordner:

```
html2pdf/bin/
```

Vorteile:

- keine Installation notwendig  
- keine PATH‑Einträge  
- portabel  
- funktioniert ohne Administratorrechte  

---

## 📦 Installation

### 1. Repository klonen

```bash
git clone https://github.com/carosaar/html2pdf.git
cd html2pdf
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Paket installieren

```bash
pip install .
```

---

## 📁 Projektstruktur

```text
html2pdf/
 ├── core/
 │    ├── converter.py
 │    ├── file_utils.py
 │    ├── wkhtmltopdf_check.py
 │
 ├── gui/
 │    └── gui_app.py
 │
 ├── cli/
 │    └── cli_app.py
 │
 ├── assets/
 │    └── html2pdf.ico
 │
 ├── bin/
 │    ├── wkhtmltopdf.exe
 │    └── libwkhtmltox.dll
 │
 ├── version.py
 └── ...
```

---

## 📄 Lizenz

- html2pdf: MIT‑Lizenz  
- wkhtmltopdf: LGPL‑3.0 (unveränderte portable Version wird mitgeliefert)

---

## 👤 Autor

(c) 2026 Dieter Eckstein

---

## ⭐ Feedback

Wenn dir das Tool gefällt, freue ich mich über ein ⭐ auf GitHub!
