"""
GUI-Frontend (Tkinter) – Version 0.2.0
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os

from html2pdf.core.file_utils import build_output_path
from html2pdf.core.converter import convert_single_html
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__


# ---------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------
SPINNER_SPEED = 600  # ms – Animationstempo (höher = ruhiger)


# ---------------------------------------------------------
# Drag & Drop Unterstützung (optional)
# ---------------------------------------------------------
def try_enable_drag_and_drop(widget, on_drop_callback):
    try:
        import tkinterdnd2 as tkdnd  # type: ignore
    except ImportError:
        return

    widget.drop_target_register(tkdnd.DND_FILES)
    widget.dnd_bind("<<Drop>>", lambda e: on_drop_callback(widget.tk.splitlist(e.data)))


# ---------------------------------------------------------
# GUI Hauptfunktion
# ---------------------------------------------------------
def run_gui():
    # ---------------------------------------------------------
    # TkinterDnD sicher initialisieren
    # ---------------------------------------------------------
    try:
        import tkinterdnd2 as tkdnd
        app = tkdnd.TkinterDnD.Tk()   # WICHTIG: richtige Tk-Klasse
        DND_AVAILABLE = True
    except Exception:
        app = tk.Tk()
        DND_AVAILABLE = False

    app.title(f"HTML → PDF Converter (v{__version__})")
    app.geometry("800x600")

    # App-Icon einbinden
    try:
        icon_path = Path(__file__).resolve().parent.parent / "assets" / "html2pdf.ico"
        if icon_path.is_file():
            app.iconbitmap(icon_path)
    except Exception:
        pass

    # Style für auffälligen Konvertieren-Button
    style = ttk.Style()
    style.configure(
        "Convert.TButton",
        font=("Segoe UI", 12, "bold"),
        padding=12,
    )

    # Arbeitsordner bestimmen
    current_root = Path(os.getcwd())

    files: list[dict] = []  # {"html": Path, "pdf": Path, "status": str}
    output_folder = tk.StringVar(value="")

    # -----------------------------------------------------
    # Hilfsfunktionen
    # -----------------------------------------------------
    def make_relative(path: Path) -> str:
        """
        Gibt einen relativen Pfad zurück, wenn möglich.
        Beginnt immer mit .\  (z. B. .\sub\ordner)
        Wenn außerhalb des Arbeitsordners → absoluter Pfad.
        """
        try:
            rel = path.relative_to(current_root)
            rel_str = str(rel)
            if rel_str == "":
                return ".\\"
            return ".\\" + rel_str.replace("/", "\\") + "\\"
        except ValueError:
            return str(path) + "\\"

    def refresh_tree():
        tree.delete(*tree.get_children())
        for idx, entry in enumerate(files):
            html_path: Path = entry["html"]
            pdf_path: Path = entry["pdf"]
            status_text: str = entry["status"]

            tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(
                    html_path.name,
                    make_relative(html_path.parent),
                    pdf_path.name,
                    make_relative(pdf_path.parent),
                    status_text,
                ),
            )

        total_label.config(text=f"Gesamt: {len(files)} Datei(en)")

    def add_files_dialog():
        paths = filedialog.askopenfilenames(filetypes=[("HTML Dateien", "*.html;*.htm")])
        if not paths:
            return
        add_files_from_paths(paths)

    def add_files_from_paths(paths):
        for p in paths:
            p = Path(p)
            if not p.is_file():
                continue
            pdf_path = build_output_path(p, output_folder.get() or None)
            files.append(
                {
                    "html": p,
                    "pdf": pdf_path,
                    "status": "Bereit",
                }
            )
        refresh_tree()

    def remove_selected():
        selection = tree.selection()
        if not selection:
            return
        indices = sorted((int(i) for i in selection), reverse=True)
        for idx in indices:
            if 0 <= idx < len(files):
                del files[idx]
        refresh_tree()

    def on_tree_double_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        idx = int(item)
        if 0 <= idx < len(files):
            del files[idx]
            refresh_tree()


    def choose_output_folder():
        folder = filedialog.askdirectory()
        if folder:
            output_folder.set(folder)
            for entry in files:
                html_path: Path = entry["html"]
                entry["pdf"] = build_output_path(html_path, output_folder.get())
            refresh_tree()

    def show_info():
        msg = (
            "HTML → PDF Converter\n\n"
            "Dieses Programm verwendet wkhtmltopdf zur Konvertierung.\n"
            "Bitte stellen Sie sicher, dass wkhtmltopdf installiert ist\n"
            "und im PATH liegt.\n\n"
            "Download: https://wkhtmltopdf.org/downloads.html\n\n"
            "Hinweise:\n"
            "- Die CLI-Version kann über 'html2pdf --help' aufgerufen werden.\n"
            "- Protokollierung ist in der CLI über die Option --log verfügbar.\n"
        )
        messagebox.showinfo("Information", msg)

    # -----------------------------------------------------
    # Konvertierung
    # -----------------------------------------------------
    def start_conversion():
        try:
            ensure_wkhtmltopdf_or_raise()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            return

        if not files:
            messagebox.showwarning("Hinweis", "Keine Dateien in der Liste.")
            return

        progress["maximum"] = len(files)
        progress["value"] = 0
        progress.config(mode="indeterminate")
        progress.start(SPINNER_SPEED)

        status_var.set("Konvertierung läuft...")
        convert_button.config(state="disabled")

        def worker():
            total = len(files)
            for idx, entry in enumerate(files):
                html_path: Path = entry["html"]
                pdf_path: Path = entry["pdf"]

                entry["status"] = "In Arbeit..."
                app.after(
                    0,
                    lambda i=idx, h=html_path: (
                        status_var.set(f"Konvertiere ({i+1}/{total}): {h.name}"),
                        refresh_tree(),
                    ),
                )

                code, stdout, stderr = convert_single_html(html_path, pdf_path)

                if code != 0:
                    first_line = stderr.splitlines()[0] if stderr else "Unbekannter Fehler"
                    entry["status"] = f"Fehler: {first_line}"
                    app.after(
                        0,
                        lambda p=html_path, s=stderr: messagebox.showerror(
                            "Fehler",
                            f"Fehler bei {p.name}:\n{s or 'Unbekannter Fehler'}",
                        ),
                    )
                else:
                    entry["status"] = "Fertig ✔"

                app.after(0, refresh_tree)

            def finish():
                progress.stop()
                progress.config(mode="determinate")
                progress["value"] = progress["maximum"]
                status_var.set("Alle Dateien verarbeitet.")
                convert_button.config(state="normal")
                messagebox.showinfo("Fertig", "Konvertierung abgeschlossen.")

            app.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------
    main_frame = ttk.Frame(app, padding=10)
    main_frame.pack(fill="both", expand=True)

    # Arbeitsordner anzeigen
    root_label = ttk.Label(
        main_frame,
        text=f"Aktueller Arbeitsordner: {current_root}",
        foreground="gray",
    )
    root_label.pack(fill="x", pady=(0, 5))

    # Obere Leiste
    top_frame = ttk.Frame(main_frame)
    top_frame.pack(fill="x")

    ttk.Button(
        top_frame,
        text="📥 HTML-Dateien hinzufügen",
        command=add_files_dialog,
    ).pack(side="left")

    ttk.Button(
        top_frame,
        text="🗂️ Ausgabeordner wählen",
        command=choose_output_folder,
    ).pack(side="left", padx=(5, 0))

    ttk.Button(
        top_frame,
        text="❌ Ausgewählte entfernen",
        command=remove_selected,
    ).pack(side="left", padx=(5, 0))

    ttk.Button(
        top_frame,
        text="ℹ️ INFO",
        command=show_info,
    ).pack(side="right")

    # Tabelle
    columns = ("html_name", "html_dir", "pdf_name", "pdf_dir", "status")
    tree = ttk.Treeview(
        main_frame,
        columns=columns,
        show="headings",
        selectmode="extended",
    )
    tree.heading("html_name", text="HTML-Datei")
    tree.heading("html_dir", text="HTML-Ordner")
    tree.heading("pdf_name", text="PDF-Datei")
    tree.heading("pdf_dir", text="PDF-Ordner")
    tree.heading("status", text="Status")

    tree.column("html_name", width=150, anchor="w")
    tree.column("html_dir", width=200, anchor="w")
    tree.column("pdf_name", width=150, anchor="w")
    tree.column("pdf_dir", width=200, anchor="w")
    tree.column("status", width=220, anchor="w")

    tree.pack(fill="both", expand=True, pady=10)
    tree.bind("<Double-1>", on_tree_double_click)


    if DND_AVAILABLE:
        try_enable_drag_and_drop(tree, add_files_from_paths)


    total_label = ttk.Label(main_frame, text="Gesamt: 0 Datei(en)")
    total_label.pack(anchor="w")

    progress = ttk.Progressbar(main_frame, mode="determinate")
    progress.pack(fill="x", pady=5)

    status_var = tk.StringVar(value="Bereit.")
    ttk.Label(main_frame, textvariable=status_var).pack(anchor="w")

    convert_button = ttk.Button(
        main_frame,
        text="🔄 Konvertieren",
        command=start_conversion,
        style="Convert.TButton",
    )
    convert_button.pack(pady=10)

    app.mainloop()
