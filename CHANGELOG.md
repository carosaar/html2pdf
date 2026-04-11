# Changelog
Alle Änderungen an diesem Projekt werden in diesem Dokument festgehalten.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und das Projekt folgt der [Semantic Versioning](https://semver.org/) Spezifikation.

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