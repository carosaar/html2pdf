# 🟦 **README**  
html2pdf – Version 0.5.0  
GUI‑ und CLI‑Tool zur HTML‑zu‑PDF‑Konvertierung mit eingebetteter wkhtmltopdf‑Engine

**html2pdf** ist ein schnelles, portables Werkzeug zur Konvertierung von HTML‑Dateien in PDF‑Dokumente.  
Es bietet sowohl eine **grafische Benutzeroberfläche (GUI)** als auch eine **Kommandozeilen‑Schnittstelle (CLI)** und enthält eine **portable Version von wkhtmltopdf**, sodass **keine Installation** erforderlich ist.

---

# 🚀 Neuerungen in Version 0.5.0 (GUI)

### 📝 Vollständig integrierte Protokollierung
- Protokollierung kann per Checkbox aktiviert werden  
- Nutzer kann eine Logdatei auswählen  
- Wenn keine Logdatei gesetzt ist, erzeugt die GUI **automatisch** eine:
  - bei vorhandenen Dateien → im Ordner der **ersten HTML‑Datei**  
  - sonst → im **aktuellen Arbeitsordner**  
- Erzeugung erfolgt **still**, ohne Dialoge oder Unterbrechungen  
- Logdatei enthält:
  - Kopfbereich mit Datum  
  - HTML‑Pfad, PDF‑Pfad, Status  
  - Zusammenfassung am Ende  

### 🪟 Neue Protokollanzeige
- eigenes Fenster mit App‑Icon  
- Monospace‑Darstellung  
- Scrollbar  
- Buttons:
  - **📝 Protokoll öffnen** → öffnet die Datei im Standardeditor  
  - **📂 Ordner öffnen** → öffnet Explorer und **markiert die Logdatei**  
  - **❎ Schließen**

### 📂 Explorer‑Integration
- Ordner öffnen nutzt jetzt:
  ```
  explorer /select,"<pfad>"
  ```
- funktioniert zuverlässig mit:
  - langen Pfaden  
  - Leerzeichen  
  - Netzwerkpfaden (UNC)  

### 🧭 Pfadkorrekturen
- relative Pfade werden korrekt angezeigt (`.\` statt `.\.\`)  
- stabile Normalisierung der Ordnerpfade in der Dateiliste  

---

# 🖥️ GUI‑Funktionen

### 📁 Dateiverwaltung
- Mehrfachauswahl von HTML‑Dateien  
- Drag & Drop Unterstützung  
- Doppelklick zum Entfernen  
- Liste leeren  
- Anzeige des aktuellen Arbeitsordners  
- relative Pfade innerhalb des Arbeitsordners  
- automatische Pfadkorrektur  

### 🧭 Ausgabeordner
- frei wählbar  
- dynamische Aktualisierung der PDF‑Zielpfade  
- Ausgabeordner wird automatisch erstellt  
- PDFs werden ohne Rückfrage überschrieben  

### ⚙️ Konvertierung
- Nutzung der eingebetteten wkhtmltopdf‑Engine  
- Live‑Statusanzeige (stderr‑Ausgabe in Echtzeit)  
- Fortschrittsbalken mit ruhiger Animation  
- sofort wirksamer Abbrechen‑Button  
- GUI bleibt auch bei großen Dateimengen reaktionsfähig  
- Fehlerdialoge mit erster stderr‑Zeile  

### 📝 Protokollierung (Details)
- optional aktivierbar  
- automatische Logdatei‑Erzeugung  
- Logdatei wird neu geschrieben  
- Protokollanzeige mit Editor‑ und Explorer‑Integration  

Starten:

```bash
html2pdf
```

oder:

```bash
python -m html2pdf.gui
```

---

# 🖥️ CLI‑Funktionen

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

Silent‑Mode:

- keine Ausgabe  
- kein Logging  
- kein Fortschritt  

---

# 🛠️ Eingebettete wkhtmltopdf‑Engine

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

# 📦 Installation

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

# 📁 Projektstruktur

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

# 📄 Lizenz

- html2pdf: MIT‑Lizenz  
- wkhtmltopdf: LGPL‑3.0 (unveränderte portable Version wird mitgeliefert)

---

# 👤 Autor

(c) 2026 Dieter Eckstein

---

# ⭐ Feedback

Wenn dir das Tool gefällt, freue ich mich über ein ⭐ auf GitHub!

