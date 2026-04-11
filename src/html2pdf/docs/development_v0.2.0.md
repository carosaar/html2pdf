# 📘 **Entwicklungsdokumentation – Version 0.2.0**

## Überblick  
Version **0.2.0** hebt die GUI‑Version von *html2pdf* auf das funktionale Niveau der CLI.  
Die Anwendung bietet nun eine vollständige, benutzerfreundliche grafische Oberfläche mit Fortschrittsanzeige, Tabellenansicht, Drag & Drop, Fehlerdialogen und einer robusten, nicht blockierenden Konvertierungslogik.

Die CLI bleibt unverändert stabil und dient weiterhin als Referenz für Logging und Automatisierung.

---

# 📁 **Projektstruktur (Stand 0.2.0)**

Die Struktur entspricht weiterhin dem modernen `src/`‑Layout:

```
html2pdf/
│
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
│
├── src/
│   └── html2pdf/
│       ├── main.py
│       ├── version.py
│       ├── core/
│       │   ├── converter.py
│       │   ├── file_utils.py
│       │   ├── wkhtmltopdf_check.py
│       │   └── logger.py
│       ├── cli/
│       │   └── cli_app.py
│       ├── gui/
│       │   └── gui_app.py   ← vollständig überarbeitet in Version 0.2.0
│       └── assets/
│           └── html2pdf.ico
│
└── tests/
```

---

# 🚀 **Neuerungen in Version 0.2.0 (GUI‑Schwerpunkt)**

Version 0.2.0 konzentriert sich vollständig auf die Weiterentwicklung der GUI.  
Die folgenden Funktionen wurden implementiert:

---

## 1. **Echte Konvertierungslogik in der GUI**

Die GUI verwendet nun dieselbe Kernlogik wie die CLI:

- Aufruf von `convert_single_html()`
- Fehlererkennung über Rückgabecode
- Ausgabe in Zielordner oder Standardpfad
- Prüfung von `wkhtmltopdf` vor Start

Damit ist die GUI funktional gleichwertig zur CLI.

---

## 2. **Fortschrittsanzeige mit ruhiger Animation**

Die Fortschrittsanzeige wurde vollständig überarbeitet:

- **Indeterminate‑Modus** während der gesamten Konvertierung  
  → zeigt klar an, dass das Programm arbeitet  
- Animation bewusst **ruhig** (Standard: 150 ms)
- Geschwindigkeit über Variable `SPINNER_SPEED` einstellbar
Wert von 600 ist angenehm ruhig
- Fortschrittszähler in der Statuszeile:  
  `Konvertiere (3/12): index.html`

---

## 3. **Tabellenansicht statt Listbox**

Die Dateiliste wurde durch eine professionelle Tabelle (`ttk.Treeview`) ersetzt.

### Spalten:

| HTML‑Datei | HTML‑Ordner | PDF‑Datei | PDF‑Ordner | Status |
|------------|-------------|-----------|------------|--------|

### Statuswerte:

- **Bereit**
- **In Arbeit…**
- **Fertig ✔**
- **Fehler: …**

### Pfadanzeige:

- **Relativ** zum Arbeitsordner (`.\sub\ordner\`)  
- **Absolut**, wenn Datei außerhalb liegt (`D:\Downloads\`)

---

## 4. **Mehrfachauswahl & Entfernen**

- Nutzer kann beliebig viele Dateien markieren
- Entfernen erfolgt in einem Schritt
- Tabelle aktualisiert sich automatisch
- Nutzer kann auch eine Zeile per Doppelklick entfernen

---

## 5. **Anzeige des aktuellen Arbeitsordners**

Über der Tabelle wird angezeigt:

```
Aktueller Arbeitsordner: C:\Users\Dieter\Dokumente\html2pdf\
```

Dieser Pfad dient als Basis für die relative Anzeige.

---

## 6. **Ausgabeordner wählbar**

- Optionaler Zielordner
- PDF‑Pfade werden dynamisch aktualisiert
- Relative/absolute Anzeige bleibt konsistent

---

## 7. **Nicht blockierende Konvertierung (Threading)**

Die GUI bleibt vollständig reaktionsfähig:

- Konvertierung läuft in einem Worker‑Thread
- GUI‑Updates erfolgen über `app.after()`
- Keine Freezes, keine Hänger

---

## 8. **Drag & Drop Unterstützung**

- Optional über `tkinterdnd2`
- Dateien können direkt in die Tabelle gezogen werden
- Fallback: GUI funktioniert auch ohne das Modul

---

## 9. **Auffälliger „Konvertieren“-Button**

- Größer  
- Fettschrift  
- Eigener Style (`Convert.TButton`)  
- Unicode‑Icon: **🔄**

---

## 10. **Unicode‑Icons für alle Buttons**

| Funktion | Icon | Beispiel |
|----------|------|----------|
| HTML hinzufügen | 📥 | „📥 HTML‑Dateien hinzufügen“ |
| Ausgabeordner | 🗂️ | „🗂️ Ausgabeordner wählen“ |
| Entfernen | ❌ | „❌ Ausgewählte entfernen“ |
| Info | ℹ️ | „ℹ️ INFO“ |
| Konvertieren | 🔄 | „🔄 Konvertieren“ |

---

## 11. **Info‑Dialog**

Der Info‑Dialog enthält:

- Hinweis auf wkhtmltopdf  
- Download‑Link  
- Hinweis auf CLI  
- Hinweis auf Protokollierung (`--log`)  

---

## 12. **App‑Icon eingebunden**

Das Icon:

```
src/html2pdf/assets/html2pdf.ico
```

wird automatisch in das Fenster eingebunden.

---

# 📌 **Zusammenfassung**

Version **0.2.0** macht die GUI:

- **voll funktionsfähig**
- **benutzerfreundlich**
- **übersichtlich**
- **stabil**
- **professionell**

Die GUI ist jetzt ein vollwertiges Frontend für die HTML‑zu‑PDF‑Konvertierung und steht funktional auf einer Stufe mit der CLI.

---

für Version 0.2.1, inklusive:
* Beenden‑Button (oben rechts)
* Abbrechen‑Button (unten, neben „Konvertieren“)
* Thread‑Stop‑Mechanismus (cancel_requested)
* Stabilisierte GUI‑Updates (keine Überflutung bei 14.000 Dateien)
* Ruhige Animation (SPINNER_SPEED)
* Drag & Drop nur bei korrekt initialisiertem TkinterDnD
* Alle Features aus 0.2.0 vollständig enthalten
