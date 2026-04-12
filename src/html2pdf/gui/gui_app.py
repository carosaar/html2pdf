"""
GUI-Frontend (Tkinter) – Version 0.3.0
Mit sofort abbrechbarer Konvertierung.
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import time

from html2pdf.core.file_utils import build_output_path
from html2pdf.core.converter import start_wkhtmltopdf, run_and_wait
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__


SPINNER_SPEED = 150  # ms – Animationstempo


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
    # Erst normales Tk erzeugen (wichtig!)
    app = tk.Tk()

    # TkinterDnD NACHTRÄGLICH aktivieren
    try:
        import tkinterdnd2 as tkdnd
        tkdnd.TkinterDnD._require(app)   # <<< entscheidend: bindet DnD an bestehendes Root
        DND_AVAILABLE = True
    except Exception:
        DND_AVAILABLE = False

    app.title(f"HTML → PDF Converter {__version__}")
    app.geometry("900x650")

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
    cancel_requested = False
    current_process = None  # laufender wkhtmltopdf-Prozess

    # -----------------------------------------------------
    # Hilfsfunktionen
    # -----------------------------------------------------
    def make_relative(path: Path) -> str:
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

    def clear_list():
        files.clear()
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

    def request_cancel():
        nonlocal cancel_requested, current_process
        cancel_requested = True
        status_var.set("Abbruch angefordert…")

        if current_process and current_process.poll() is None:
            try:
                # Sauberer Abbruch wie CTRL+C
                current_process.send_signal(signal.CTRL_BREAK_EVENT)
            except Exception:
                # Fallback: hart killen
                current_process.kill()


    def request_exit():
        if convert_button["state"] == "disabled":
            messagebox.showwarning("Hinweis", "Bitte zuerst die Konvertierung abbrechen.")
            return
        app.destroy()

    # -----------------------------------------------------
    # Konvertierung
    # -----------------------------------------------------
    def start_conversion():
        nonlocal cancel_requested, current_process
        cancel_requested = False
        current_process = None

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

        status_var.set("Konvertierung läuft…")
        convert_button.config(state="disabled")
        cancel_button.config(state="normal")
        exit_button.config(state="disabled")

        def worker():
            nonlocal current_process

            total = len(files)
            for idx, entry in enumerate(files):

                if cancel_requested:
                    entry["status"] = "Abgebrochen"
                    app.after_idle(refresh_tree)
                    break

                html_path: Path = entry["html"]
                pdf_path: Path = entry["pdf"]

                entry["status"] = "In Arbeit…"
                app.after_idle(refresh_tree)

                # Prozess starten
                process = start_wkhtmltopdf(html_path, pdf_path)
                current_process = process

                # Prozess überwachen
                while process.poll() is None:
                    if cancel_requested:
                        try:
                            process.terminate()
                        except Exception:
                            pass
                        entry["status"] = "Abgebrochen"
                        app.after_idle(refresh_tree)
                        break
                    time.sleep(0.1)

                if cancel_requested:
                    break

                # Ergebnis auslesen
                code, stdout, stderr = run_and_wait(process)

                if code != 0:
                    first_line = stderr.splitlines()[0] if stderr else "Unbekannter Fehler"
                    entry["status"] = f"Fehler: {first_line}"
                else:
                    entry["status"] = "Fertig ✔"

                if idx % 20 == 0:
                    app.after_idle(refresh_tree)

                if idx % 10 == 0:
                    app.after_idle(lambda i=idx: status_var.set(f"Verarbeitet: {i+1}/{total}"))

            def finish():
                progress.stop()
                progress.config(mode="determinate")
                progress["value"] = progress["maximum"]

                if cancel_requested:
                    status_var.set("Konvertierung abgebrochen.")
                    app.bell()
                    messagebox.showinfo("Abgebrochen", "Die Konvertierung wurde abgebrochen.")
                else:
                    status_var.set("Alle Dateien verarbeitet.")

                convert_button.config(state="normal")
                cancel_button.config(state="disabled")
                exit_button.config(state="normal")
                refresh_tree()

            app.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------
    main_frame = ttk.Frame(app, padding=10)
    main_frame.pack(fill="both", expand=True)

    root_label = ttk.Label(
        main_frame,
        text=f"Aktueller Arbeitsordner: {current_root}",
        foreground="gray",
    )
    root_label.pack(fill="x", pady=(0, 5))

    # Obere Leiste
    top_frame = ttk.Frame(main_frame)
    top_frame.pack(fill="x")

    ttk.Button(top_frame, text="📥 HTML-Dateien hinzufügen", command=add_files_dialog).pack(side="left")
    ttk.Button(top_frame, text="🗂️ Ausgabeordner wählen", command=choose_output_folder).pack(side="left", padx=(5, 0))
    ttk.Button(top_frame, text="❌ Ausgewählte entfernen", command=remove_selected).pack(side="left", padx=(5, 0))
    ttk.Button(top_frame, text="🗑️ Liste leeren", command=clear_list).pack(side="left", padx=(5, 0))

    exit_button = ttk.Button(top_frame, text="Beenden", command=request_exit)
    exit_button.pack(side="right")

    ttk.Button(top_frame, text="ℹ️ INFO", command=show_info).pack(side="right", padx=(0, 5))

    # Tabelle + Scrollbar
    table_frame = ttk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True, pady=10)

    columns = ("html_name", "html_dir", "pdf_name", "pdf_dir", "status")
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="extended",
        height=18,
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

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    tree.bind("<Double-1>", on_tree_double_click)

    if DND_AVAILABLE:
        try_enable_drag_and_drop(tree, add_files_from_paths)

    total_label = ttk.Label(main_frame, text="Gesamt: 0 Datei(en)")
    total_label.pack(anchor="w")

    progress = ttk.Progressbar(main_frame, mode="determinate")
    progress.pack(fill="x", pady=5)

    status_var = tk.StringVar(value="Bereit.")
    ttk.Label(main_frame, textvariable=status_var).pack(anchor="w")

    # Untere Leiste
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill="x", pady=(10, 0))

    convert_button = ttk.Button(
        bottom_frame,
        text="🔄 Konvertieren",
        command=start_conversion,
        style="Convert.TButton",
    )
    convert_button.pack(side="left")

    cancel_button = ttk.Button(
        bottom_frame,
        text="⛔ Abbrechen",
        command=request_cancel,
        state="disabled",
    )
    cancel_button.pack(side="left", padx=(10, 0))

    # -----------------------------------------------------
    # Fenster schließen abfangen – jetzt existieren alle Widgets
    # -----------------------------------------------------
    def on_close():
        if convert_button["state"] == "disabled":
            if messagebox.askyesno(
                "Konvertierung läuft",
                "Es läuft gerade eine Konvertierung.\nSoll sie abgebrochen und das Programm geschlossen werden?"
            ):
                request_cancel()
                app.after(200, on_close)
            return
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)

    app.mainloop()