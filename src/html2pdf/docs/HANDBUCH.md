Alles klar, Dieter — hier kommt **das vollständige Handbuch**, exakt nach deiner gewünschten Gliederung, **mit klickbaren Markdown‑Links**, vollständig ausgearbeitet, sauber strukturiert und sofort nutzbar als `HANDBUCH.md`.

Ich habe darauf geachtet:

- klare, professionelle Struktur  
- vollständige Beschreibung aller GUI‑Funktionen  
- neue Protokollierung + Protokollanzeige vollständig integriert  
- CLI‑Teil kompakt, aber vollständig  
- keine Wiederholungen  
- technisch präzise, aber gut lesbar  

---

# 🟦 **HANDBUCH – html2pdf**

## 📑 **Inhaltsverzeichnis**

1. [Einleitung](#1-einleitung)  
2. [Installation & Start](#2-installation--start)  
3. [Überblick über die Benutzeroberfläche (GUI)](#3-überblick-über-die-benutzeroberfläche-gui)  
4. [Arbeiten mit Dateien](#4-arbeiten-mit-dateien)  
5. [Ausgabeoptionen](#5-ausgabeoptionen)  
6. [Konvertierungsvorgang](#6-konvertierungsvorgang)  
7. [Protokollierung (GUI)](#7-protokollierung-gui)  
8. [Protokollanzeige](#8-protokollanzeige)  
9. [Kommandozeilen‑Modus (CLI)](#9-kommandozeilen-modus-cli)  
10. [Fehlerbehebung (Troubleshooting)](#10-fehlerbehebung-troubleshooting)  
11. [Tipps & Best Practices](#11-tipps--best-practices)  
12. [Anhang](#12-anhang)  

---

# 1. Einleitung

**html2pdf** ist ein portables Werkzeug zur Konvertierung von HTML‑Dateien in PDF‑Dokumente.  
Es bietet:

- eine **moderne, reaktionsfähige GUI**  
- eine **vollwertige CLI**  
- eine **eingebettete portable wkhtmltopdf‑Engine**  
- keine Installation, keine Administratorrechte  

**Zielgruppe:**  
Anwender, die HTML‑Dateien schnell, zuverlässig und ohne Konfigurationsaufwand in PDF umwandeln möchten.

**Systemvoraussetzungen:**  
- Windows 10 oder neuer  
- Python 3.10+ (bei Nutzung aus dem Quellcode)  
- Keine Installation von wkhtmltopdf erforderlich  

---

# 2. Installation & Start

## 2.1 Repository klonen

```bash
git clone https://github.com/carosaar/html2pdf.git
cd html2pdf
```

## 2.2 Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## 2.3 Start der GUI

```bash
html2pdf
```

oder:

```bash
python -m html2pdf.gui
```

## 2.4 Start der CLI

```bash
python -m html2pdf.cli
```

## 2.5 Portable Nutzung

Die portable wkhtmltopdf‑Engine befindet sich in:

```
html2pdf/bin/
```

Keine Installation notwendig.

---

# 3. Überblick über die Benutzeroberfläche (GUI)

Die GUI besteht aus:

- **Buttonleiste oben** (Dateien hinzufügen, Ausgabeordner wählen, Liste leeren, Beenden)  
- **Dateiliste** (HTML‑Dateien, Ordner, Ziel‑PDF, Status)  
- **Arbeitsordneranzeige**  
- **Konvertieren‑Button**  
- **Fortschrittsbalken**  
- **Statuszeile**  
- **Protokollierungsoptionen**  

---

# 4. Arbeiten mit Dateien

## 4.1 HTML‑Dateien hinzufügen
- über Dateidialog  
- per Drag & Drop  

## 4.2 Drag & Drop
Unterstützt, wenn `tkinterdnd2` installiert ist.

## 4.3 Dateien entfernen
Doppelklick auf eine Zeile entfernt die Datei.

## 4.4 Liste leeren
Button „Liste leeren“.

## 4.5 Pfaddarstellung
- Dateien im Arbeitsordner → `.\`  
- Unterordner → `.\unterordner\`  
- außerhalb → absoluter Pfad  

## 4.6 Pfadlogik
- automatische Normalisierung  
- keine `.\.\`‑Artefakte  
- stabile Darstellung auch bei Netzwerkpfaden  

---

# 5. Ausgabeoptionen

## 5.1 Ausgabeordner wählen
Der Zielordner kann frei gewählt werden.

## 5.2 Automatische PDF‑Benennung
PDF‑Name = HTML‑Basename + `.pdf`.

## 5.3 Verhalten bei bestehenden Dateien
PDFs werden ohne Rückfrage überschrieben.

## 5.4 Erstellen fehlender Ordner
Fehlende Ausgabeordner werden automatisch erzeugt.

---

# 6. Konvertierungsvorgang

## 6.1 Start der Konvertierung
Über den Button **Konvertieren**.

## 6.2 Live‑Status
stderr‑Ausgabe von wkhtmltopdf wird live angezeigt.

## 6.3 Fortschrittsbalken
Ruhige Animation, unabhängig von Dateigröße.

## 6.4 Abbrechen
Der Abbrechen‑Button stoppt die Konvertierung sofort.

## 6.5 Verhalten bei Fehlern
- Fehlerdialog mit erster stderr‑Zeile  
- Status in der Tabelle wird aktualisiert  

## 6.6 Performance‑Hinweise
- GUI bleibt auch bei tausenden Dateien reaktionsfähig  
- Statusupdates sind gedrosselt  

---

# 7. Protokollierung (GUI)

## 7.1 Aktivieren der Protokollierung
Checkbox „Protokollierung aktivieren“.

## 7.2 Auswahl einer Logdatei
Über Dateidialog möglich.

## 7.3 Automatische Logdatei‑Erzeugung
Wenn kein Logdateiname gesetzt ist:

### 7.3.1 Ordner der ersten HTML‑Datei  
→ wenn Dateien in der Liste stehen

### 7.3.2 Fallback: aktueller Arbeitsordner  
→ wenn die Liste leer ist

### 7.3.3 Still, ohne Dialoge  
→ keine Unterbrechung des Workflows

## 7.4 Inhalt der Logdatei
- Datum  
- HTML‑Pfad  
- PDF‑Pfad  
- Status  
- Zusammenfassung  

## 7.5 Speicherort & Format
- Textdatei (`.txt`)  
- UTF‑8  

---

# 8. Protokollanzeige

## 8.1 Öffnen der Protokollanzeige
Nach der Konvertierung über den Button „Protokoll anzeigen“.

## 8.2 Aufbau des Fensters
- Monospace‑Textfeld  
- Scrollbar  
- App‑Icon  

## 8.3 Funktionen

### 8.3.1 📝 Protokoll öffnen  
Öffnet die Logdatei im Standardeditor (`os.startfile()`).

### 8.3.2 📂 Ordner öffnen  
Öffnet den Explorer und markiert die Logdatei:

```
explorer /select,"<pfad>"
```

### 8.3.3 ❎ Schließen  
Schließt das Fenster.

## 8.4 Explorer‑Integration
Robust auch bei langen Pfaden, Leerzeichen und UNC‑Pfaden.

## 8.5 Typische Fehler & Lösungen
- Datei existiert nicht → Logdatei wurde gelöscht  
- Explorer öffnet nicht → Pfad enthält ungültige Zeichen  

---

# 9. Kommandozeilen‑Modus (CLI)

## 9.1 Aufruf

```bash
html2pdf --input input.html --output out/
```

## 9.2 Parameterübersicht

```
--input <datei/ordner>
--output <ordner>
--silent
--log <optional: logfile>
```

## 9.3 Beispiele

```bash
html2pdf -i *.html -o out/
```

## 9.4 Silent‑Mode
- keine Ausgabe  
- kein Fortschritt  
- kein Logging  

## 9.5 Logging im CLI
Optional über `--log`.

## 9.6 Unterschiede zur GUI
- keine Live‑Statusanzeige  
- keine Protokollanzeige  

---

# 10. Fehlerbehebung (Troubleshooting)

## 10.1 wkhtmltopdf nicht gefunden
→ interne Engine wird automatisch genutzt.

## 10.2 Keine Schreibrechte
→ Ausgabeordner ändern.

## 10.3 Fehlerhafte HTML‑Dateien
→ Browser‑Vorschau testen.

## 10.4 Netzwerkpfade / UNC‑Pfade
→ Explorer‑Integration funktioniert, aber Schreibrechte prüfen.

## 10.5 Logdatei kann nicht geöffnet werden
→ Datei existiert? Pfad korrekt?

## 10.6 Explorer öffnet nicht
→ Sonderzeichen im Pfad entfernen.

---

# 11. Tipps & Best Practices

## 11.1 Strukturierung großer HTML‑Sammlungen
Ordnerstruktur nutzen.

## 11.2 Optimale Ausgabeordner
Pro Projekt ein eigener Ordner.

## 11.3 Umgang mit sehr großen Dateien
Protokollierung aktivieren.

## 11.4 Nutzung der Protokollierung
Ideal zur Fehlersuche.

---

# 12. Anhang

## 12.1 Versionshistorie
Siehe CHANGELOG.md.

## 12.2 Projektstruktur

```
html2pdf/
 ├── core/
 ├── gui/
 ├── cli/
 ├── assets/
 ├── bin/
 └── version.py
```

## 12.3 Lizenztexte
MIT‑Lizenz, LGPL‑3.0 für wkhtmltopdf.

## 12.4 Kontakt / Support
(c) 2026 Dieter Eckstein

---

Wenn du möchtest, kann ich dir jetzt:

- eine **PDF‑Version** des Handbuchs generieren (als Markdown‑Text, nicht als Datei)  
- eine **Kurzversion** für Endanwender erstellen  
- oder das Handbuch in **mehrere Dateien** aufteilen (z. B. `/docs/`)
