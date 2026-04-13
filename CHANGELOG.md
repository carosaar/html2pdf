# Changelog

Alle Änderungen an diesem Projekt werden in diesem Dokument festgehalten.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und das Projekt folgt der [Semantic Versioning](https://semver.org/) Spezifikation.


## 0.4.1 – 2026‑04‑13
### Fixes
- **Deadlock bei großen HTML‑Dateien behoben**  
  - Ursache: wkhtmltopdf erzeugt umfangreiche stderr‑Ausgaben, die bei Nutzung von `PIPE` ohne kontinuierliches Auslesen zum Pufferüberlauf führten.  
  - Lösung: stderr wird nun nur im GUI‑ und nicht‑silent‑CLI‑Modus gepuffert und in einem separaten Thread ausgelesen.  
  - CLI - Silent‑Mode nutzt `stderr=DEVNULL`, wodurch keine Ausgabe entsteht und kein Deadlock mehr möglich ist.

- **Silent‑Mode vollständig korrigiert**  
  - Keine Fortschrittsmeldungen mehr auf stdout/stderr  
  - Keine Startmeldung mehr („Starte html2pdf Version …“)  
  - Kein implizites Flushen von stderr mehr  
  - Prozess läuft jetzt vollständig geräuschlos durch

- **Logging überarbeitet und erweitert** (dies wird jedoch nochmal ganz neu geplant)
  - Logdatei wird **neu geschrieben**, nicht mehr angehängt  
  - Automatische Logdatei: `<basename>_log.txt`  
  - Pro Datei werden nun protokolliert:
    - Vollständiger Pfad der Eingabedatei  
    - Vollständiger Pfad der erzeugten PDF  
    - Fehler mit vollständigem Pfad  
    - Trennzeile `---` nach jeder Datei  

- **GUI: Live‑Fortschrittsanzeige aus wkhtmltopdf**
  - stderr‑Ausgabe wird in Echtzeit in der Statuszeile angezeigt  
  - Kein Deadlock mehr  
  - Abbruchfunktion bleibt sofort wirksam  
  - Große Dateien funktionieren zuverlässig

### Intern
- `converter.py` erweitert um `capture_stderr`‑Parameter  
- CLI‑Verarbeitung neu strukturiert  
- logger.py überarbeitet: keine stdout‑Handler mehr, Startmeldung nur bei Datei‑Logging  
  
---
 
## 0.4.0 – Eingebettete wkhtmltopdf‑Engine (Standalone‑Modus) 2026-04-12

### Neu
- html2pdf enthält nun eine **eingebettete portable Version von wkhtmltopdf**  
  (`wkhtmltopdf.exe` + `libwkhtmltox.dll`).  
  Dadurch funktioniert html2pdf **ohne Installation** von wkhtmltopdf und ohne PATH‑Eintrag.
- Automatische Erkennung:  
  html2pdf nutzt bevorzugt die interne Version, fällt aber bei Bedarf auf eine Systeminstallation zurück.

### Verbessert
- Stabilere Pfadlogik für portable Builds (PyInstaller‑kompatibel).
- Vereinheitlichte Fehlerbehandlung, falls weder interne noch externe wkhtmltopdf‑Version verfügbar ist.

### Intern
- Neuer Mechanismus zur Pfadauflösung (`wkhtmltopdf_check.py`).
- Spec‑Datei erweitert, um die portable wkhtmltopdf‑Engine einzubetten.

## 0.3.0 – Verbesserte Prozesssteuerung & stabilere GUI 2026-04-12

### Neu
- Sofortiger Abbruch laufender Konvertierungen: Der `wkhtmltopdf`‑Prozess wird nun unmittelbar beendet, sobald der Benutzer „Abbrechen“ auswählt.
- Verbesserte Prozessüberwachung: Die GUI reagiert unmittelbar auf Statusänderungen und bleibt auch bei vielen Dateien flüssig.

### Verbessert
- Der **Beenden‑Button** ist während einer laufenden Konvertierung deaktiviert, um unbeabsichtigtes Schließen zu verhindern.
- Stabilere GUI‑Interaktion während der Konvertierung (Statusupdates, Fortschrittsanzeige, Responsiveness).

### Intern
- Überarbeitete Prozesslogik für Start, Überwachung und Abbruch.
- Vereinheitlichte Statusmeldungen und Fehlerbehandlung.

## [0.2.2] - 2026-04-11

### Behoben

CLI-Parameter `--output` wurde immer als **Zielverzeichnis** interpretiert.
**Ursache**: Bei einem einzelnen HTML-Eingabepfad wie 

```
html2pdf.exe --input .\input.html --output .\Ausgabe.pdf
``` 

wurde intern versucht, in Ausgabe.pdf\input.pdf zu schreiben.

**Fix**:
>`build_output_path()` erkennt jetzt, wenn `--output` eine einzelne .pdf-Datei ist, und verwendet diesen Pfad direkt.
Bei mehreren Eingabedateien führt `--output` als einzelne PDF-Datei jetzt zu einer klaren Fehlermeldung.

**Ergebnis**: 
>CLI-Aufrufe mit explizitem PDF-Ziel funktionieren jetzt korrekt, ohne dass wkhtmltopdf wegen eines ungültigen Ausgabepfads abbricht.

**Hinweis**:
>Für den PyInstaller-Build wurde außerdem ein Runtime-Hook (`pyi_rth_attach_console.py`) eingeführt. Dieser sorgt dafür, dass die gebaute EXE bei normalem Start ohne Argumente als GUI startet, aber bei CLI-Argumenten eine Konsole öffnet und UTF-8-Ausgabe unterstützt.

## [0.2.1] – 2026‑04‑11

### Hinzugefügt

- Beenden‑Button in der oberen Buttonleiste (schließt die Anwendung, wenn keine Konvertierung läuft).
- Abbrechen‑Button in der unteren Leiste, um eine laufende Konvertierung kontrolliert zu stoppen.
- Button und Funktion `Liste leeren` in der oberen Buttleiste entfernt alle Dateieinträge in der Tabelle
- Thread‑Stop‑Mechanismus (`cancel_requested`) zur sicheren Unterbrechung großer Konvertierungsjobs.
- Vertikaler Scrollbalken in der Dateiliste

### Geändert

- Fortschritts- und Statusaktualisierung gedrosselt, um Überlastung der GUI‑Eventqueue bei sehr vielen Dateien zu verhindern.
- Statusmeldungen werden nun nur noch bei relevanten Änderungen aktualisiert.
- Indeterminate‑Animation läuft stabil bis zum tatsächlichen Ende oder Abbruch der Konvertierung.

### Behoben

- Problem, bei dem die GUI während großer Konvertierungsjobs (z. B. 14.000 Dateien) nicht mehr bedienbar war.
- Problem, bei dem Statusmeldungen zu früh „Fertig“ anzeigten, obwohl die Konvertierung noch lief.

---

## [0.2.0] – 2026‑04‑11

### Hinzugefügt

- Vollständig überarbeitete GUI mit funktionaler Gleichstellung zur CLI.
- Tabellenansicht (ttk.Treeview) mit Spalten:
  - HTML‑Datei
  - HTML‑Ordner (relativ zu Arbeitsordner, beginnend mit .\)
  - PDF‑Datei
  - PDF‑Ordner
  - Status (Bereit, In Arbeit…, Fertig ✔, Fehler)
- Anzeige des aktuellen Arbeitsordners über der Tabelle.
- Unterstützung für Drag & Drop (optional, wenn tkinterdnd2 verfügbar ist).
- Doppelklick auf Tabellenzeile entfernt die Datei aus der Liste.
- Auswahl eines Ausgabeordners mit dynamischer Aktualisierung der PDF‑Pfade.
- Fortschrittsanzeige mit ruhiger Indeterminate‑Animation (Geschwindigkeit über Variable SPINNER_SPEED einstellbar).
- Statuszeile mit Fortschrittszähler (z. B. „Konvertiere (3/12): index.html“).
- Unicode‑Icons für alle Buttons (📥, 🗂️, ❌, ℹ️, 🔄).
- Auffälliger „Konvertieren“-Button (größer, fett, eigener Style).
- Einbindung des App‑Icons `html2pdf.ico`.

### Geändert

- Konvertierungslogik der GUI vollständig auf die Core‑Funktionen abgestimmt.
- Threading überarbeitet: GUI bleibt während der gesamten Konvertierung reaktionsfähig.
- Fehlerdialoge verbessert (inkl. erster Fehlermeldung aus stderr).
- Pfadanzeige überarbeitet: relative Pfade nur innerhalb des Arbeitsordners, sonst absolute Pfade.

### Behoben

- Fehler bei Drag & Drop, wenn tkinterdnd2 installiert, aber nicht korrekt initialisiert war (TkinterDnD.Tk wird nun sicher verwendet).
- Animation wurde zuvor nur bei der ersten Datei angezeigt – läuft jetzt durchgehend.

### Hinweise

- Protokollierung weiterhin über CLI verfügbar (`--log`).

---

## [0.1.0] – 2026-04-11

### Hinzugefügt

- Vollständige **CLI-Version** mit:
  - Verarbeitung einzelner HTML-Dateien
  - Verarbeitung aller HTML-Dateien eines Ordners
  - Ausgabe in Zielordner oder Quellordner
  - Logging-System mit zentraler Versionsausgabe
  - Prüfung der Installation von `wkhtmltopdf`
  - Fehlerbehandlung und Exit-Codes
  - **Animiertem Spinner** während der Konvertierung
  - Silent-Mode (`--silent`)
  - Logdatei-Option (`--log`)

- **Projektstruktur** im modernen `src/`-Layout:
  - Trennung von Core, CLI, GUI und Dokumentation
  - Zentrale Versionsdatei `version.py`
  - Dynamische Versionierung über `pyproject.toml`

- **GUI-Grundgerüst** (Tkinter):
  - Dateiauswahl
  - Dateiliste
  - Fortschrittsbalken
  - Statusanzeige
  - Threading-Vorbereitung
  - Prüfung von `wkhtmltopdf`

- **GitHub-Projekteinrichtung**:
  - `.gitignore`
  - MIT-Lizenz (inkl. deutscher Übersetzung)
  - README-Snippet
  - Dokumentation des Entwicklungsstands

### Geändert

- Absolute Paketimporte eingeführt, um Installationsfehler zu vermeiden.
- Logging verbessert und um Versionsausgabe erweitert.

### Bekannte Einschränkungen

- GUI führt noch keine echte Konvertierung durch.
- Keine rekursive Ordnersuche in der CLI.
- Keine Konfigurationsdatei.
- Keine Installer/Standalone-Version.

---

## [Unveröffentlicht]

### Geplant
- GUI-Konvertierung (Version 0.2.0)
- Erweiterte CLI-Funktionen (Version 0.3.0)
- Konfigurationssystem (Version 0.4.0)
- Installer & Distribution (Version 0.5.0)
- Stabiler Release 1.0.0