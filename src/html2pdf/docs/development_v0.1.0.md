Hier ist eine **professionelle, klar strukturierte Dokumentation** des aktuellen Entwicklungsstands deines Projekts **html2pdf – Version 0.1.0**.  
Sie ist so formuliert, dass du sie direkt in dein Repository (z. B. als `docs/development_v0.1.0.md`) übernehmen kannst.

---

# 📘 **Entwicklungsdokumentation – Version 0.1.0**

## Überblick  
Version **0.1.0** stellt den ersten funktionsfähigen Entwicklungsstand des Projekts *html2pdf* dar.  
Die CLI‑Version ist vollständig lauffähig, stabil und produktiv nutzbar.  
Die GUI‑Version ist eingerichtet und funktionsfähig, benötigt jedoch noch Erweiterungen für die vollständige Konvertierungslogik und Benutzerführung.

---

# 📁 **Projektstruktur (Stand 0.1.0)**

Das Projekt folgt dem modernen **`src/`‑Layout**, wie es für Python‑Projekte auf GitHub empfohlen wird.  
Alle Module sind klar getrennt nach Verantwortlichkeiten.

```
html2pdf/
│
├── pyproject.toml          # Projektdefinition, Versionierung, Entry-Point
├── README.md               # Projektbeschreibung
├── LICENSE                 # MIT-Lizenz (inkl. deutscher Übersetzung)
├── .gitignore              # Git-Ignore-Regeln
│
├── src/
│   └── html2pdf/
│       ├── __init__.py
│       ├── main.py         # Einstiegspunkt: entscheidet zwischen GUI und CLI
│
│       ├── version.py      # Zentrale Versionsdatei (__version__ = "0.1.0")
│
│       ├── core/
│       │   ├── __init__.py
│       │   ├── converter.py          # Kernlogik: Aufruf von wkhtmltopdf
│       │   ├── file_utils.py         # Datei-/Ordnererkennung, Pfadfunktionen
│       │   ├── wkhtmltopdf_check.py  # Prüfung der Installation von wkhtmltopdf
│       │   └── logger.py             # Globales Logging inkl. Versionsausgabe
│
│       ├── cli/
│       │   ├── __init__.py
│       │   └── cli_app.py            # Vollständige CLI mit Spinner-Fortschritt
│
│       ├── gui/
│       │   ├── __init__.py
│       │   └── gui_app.py            # GUI-Grundgerüst (Tkinter)
│
│       └── docs/
│           └── help_text.md          # Benutzerhilfe (Skeleton)
│
└── tests/
    └── test_basic.py                 # Platzhalter für zukünftige Tests
```

### Kurzbeschreibung der wichtigsten Dateien

| Datei | Funktion |
|-------|----------|
| **main.py** | Startpunkt des Programms. Entscheidet automatisch zwischen GUI und CLI. |
| **version.py** | Zentrale Versionsquelle (`__version__ = "0.1.0"`). |
| **converter.py** | Führt die HTML→PDF‑Konvertierung über `wkhtmltopdf` aus. |
| **file_utils.py** | Erkennt, ob ein Pfad Datei oder Ordner ist; erzeugt Ausgabepfade. |
| **wkhtmltopdf_check.py** | Prüft, ob `wkhtmltopdf` installiert ist. |
| **logger.py** | Initialisiert Logging und schreibt die Versionsinfo. |
| **cli_app.py** | Vollständige CLI mit Spinner‑Animation und Fehlerbehandlung. |
| **gui_app.py** | GUI‑Grundstruktur mit Dateiauswahl, Fortschrittsbalken und Statusanzeige. |

---

# 🛠️ **Projekteinrichtung für GitHub**

Das Projekt ist vollständig GitHub‑ready:

### ✔ `src/`‑Layout  
- Standard für moderne Python‑Projekte  
- Verhindert Importprobleme  
- Kompatibel mit `pip install .` und `pip install -e .`

### ✔ Versionierung über `version.py`  
- Zentrale Version: `__version__ = "0.1.0"`  
- In `pyproject.toml` dynamisch eingebunden:

```toml
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "html2pdf.version.__version__"}
```

Damit ist die Version:

- in CLI und GUI sichtbar  
- im Logger dokumentiert  
- für Builds und Releases verfügbar  

### ✔ GitHub‑Dateien  
- `.gitignore` für Python, Build‑Artefakte, Installer, Logs  
- `LICENSE` (MIT + deutsche Übersetzung)  
- `README.md` (Snippet)  

### ✔ Installation über pip  
Nach `pip install .` wird automatisch ein Konsolenbefehl erzeugt:

```
html2pdf
```

Dieser ruft `html2pdf.main:main()` auf.

---

# 🚀 **Stand der Entwicklung – Version 0.1.0**

## ✔ CLI-Version – **vollständig funktionsfähig**

Die CLI unterstützt:

### **Funktionen**
- Verarbeitung einer einzelnen HTML‑Datei  
- Verarbeitung aller HTML‑Dateien eines Ordners  
- Automatische Erzeugung der PDF‑Dateinamen  
- Ausgabe in denselben Ordner oder in einen Zielordner  
- Logging in Datei oder Konsole  
- Silent‑Mode  
- Prüfung von `wkhtmltopdf`  
- Fehlerbehandlung für fehlende Dateien, fehlende Installation, Rückgabecodes  

### **Neu in 0.1.0**
- **Animierter Spinner** während der Konvertierung  
- Klare Erfolg‑/Fehlerausgabe  
- Saubere Stop‑Mechanik für den Spinner  
- Logging mit Versionsinfo  

Die CLI ist damit **produktionsreif**.

---

## 🧩 GUI-Version – **Grundgerüst steht**

Die GUI enthält:

- Hauptfenster (Tkinter)  
- Dateiauswahl  
- Dateiliste  
- Fortschrittsbalken  
- Statusanzeige  
- Threading‑Vorbereitung  
- Prüfung von `wkhtmltopdf`  
- Platzhalter für Konvertierungslogik  

### Noch offen für Version 0.2.0:
- Einbindung der echten Konvertierung  
- Fortschrittsbalken synchronisieren  
- Fehlerdialoge  
- Ausgabeordner‑Option  
- Drag & Drop (optional)  
- Benutzerfreundliche Meldungen  

---

# 📌 **Zusammenfassung**

Version **0.1.0** liefert:

- eine **vollständig funktionierende CLI**  
- eine **strukturierte, erweiterbare GUI**  
- ein **sauberes, modernes Projektlayout**  
- zentrale **Versionierung**  
- **Logging** mit Versionsausgabe  
- GitHub‑kompatible Projektdateien  
- klare Trennung von Core, CLI, GUI  

Das Projekt ist damit stabil, wartbar und bereit für die Weiterentwicklung der GUI in Version **0.2.0**.