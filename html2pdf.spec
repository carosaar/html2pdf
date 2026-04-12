# html2pdf.spec – FINAL für html2pdf v0.2.1

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

# Projekt-Root (dort wo pyinstaller ausgeführt wird)
project_root = Path(os.getcwd())

# src/ Ordner
src_root = project_root / "src"

# Einstiegspunkt: __main__.py (python -m html2pdf)
entry_script = src_root / "html2pdf" / "__main__.py"

# Icon
icon_file = src_root / "html2pdf" / "assets" / "html2pdf.ico"

# Runtime-Hook zum Anbinden der Konsole bei CLI-Argumenten
runtime_hook = project_root / "pyi_rth_attach_console.py"

# Alle html2pdf-Module automatisch einsammeln
hidden = collect_submodules("html2pdf")

a = Analysis(
    [str(entry_script)],
    pathex=[str(src_root)],   # WICHTIG: src/ als Suchpfad
    binaries=[],
    datas=[
        (str(src_root / "html2pdf" / "assets"), "html2pdf/assets"), # Assets einbinden
        (str(src_root / "html2pdf" / "bin"), "html2pdf/bin"), # wkhtmltopdf einbinden
    ],
    hiddenimports=hidden,
    hookspath=[str(project_root)],
    hooksconfig={},
    runtime_hooks=[str(runtime_hook)],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="html2pdf",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,           # Console app; runtime hook hides console in GUI mode
    icon=str(icon_file),
)
