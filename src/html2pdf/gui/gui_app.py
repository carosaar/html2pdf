"""
GUI-Frontend (Tkinter) – Version 0.5.0
Mit sofort abbrechbarer Konvertierung, Fortschrittsanzeige und optionaler Protokollierung.
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import time
import signal
import subprocess
from datetime import datetime

from html2pdf.core.file_utils import build_output_path
from html2pdf.core.converter import start_wkhtmltopdf, run_and_wait
from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__

# GUI-Logger
from html2pdf.gui.logger_gui import GuiLogger

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
    app = tk.Tk()

    # TkinterDnD aktivieren
    try:
        import tkinterdnd2 as tkdnd
        tkdnd.TkinterDnD._require(app)
        DND_AVAILABLE = True
    except Exception:
        DND_AVAILABLE = False

    app.title(f"HTML → PDF Converter {__version__}")
    app.geometry("900x650")

    # Icon
    try:
        icon_path = Path(__file__).resolve().parent.parent / "assets" / "html2pdf.ico"
        if icon_path.is_file():
            app.iconbitmap(icon_path)
    except Exception:
        pass

    # Style
    style = ttk.Style()
    style.configure(
        "Convert.TButton",
        font=("Segoe UI", 12, "bold"),
        padding=12,
    )

    current_root = Path(os.getcwd())

    files: list[dict] = []
    output_folder = tk.StringVar(value="")
    cancel_requested = False
    current_process = None

    # Logging
    log_enabled = tk.BooleanVar(value=False)
    logfile_path = tk.StringVar(value="")

    # -----------------------------------------------------
    # Hilfsfunktionen
    # -----------------------------------------------------
    
    def show_logfile_window(path):
        win = tk.Toplevel()
        win.title("Protokollanzeige")
        win.geometry("900x650")

        # Icon übernehmen
        try:
            icon_path = Path(__file__).resolve().parent.parent / "assets" / "html2pdf.ico"
            if icon_path.is_file():
                win.iconbitmap(icon_path)
        except Exception:
            pass

        # --- Hauptbereich: Text + Scrollbar ---
        text_frame = ttk.Frame(win)
        text_frame.pack(fill="both", expand=True)

        text = tk.Text(text_frame, wrap="word", font=("Consolas", 10))
        text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.configure(yscrollcommand=scrollbar.set)

        # Dateiinhalt laden
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            text.insert("1.0", content)
        except Exception as e:
            text.insert("1.0", f"Fehler beim Lesen der Logdatei:\n{e}")

        # Untere Button-Leiste (zentriert)
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", pady=10)

        inner = ttk.Frame(btn_frame)
        inner.pack()

        def open_file():
            try:
                os.startfile(path)
            except Exception as e:
                messagebox.showerror("Fehler", f"Die Datei konnte nicht geöffnet werden:\n{e}")

        def open_folder():
            try:
                subprocess.Popen(f'explorer /select,"{path}"')
            except Exception as e:
                messagebox.showerror("Fehler", f"Ordner konnte nicht geöffnet werden:\n{e}")

        ttk.Button(inner, text="📝 Protokoll öffnen", command=open_file).pack(side="left", padx=10)
        ttk.Button(inner, text="📂 Ordner öffnen", command=open_folder).pack(side="left", padx=10)
        ttk.Button(inner, text="❎ Schließen", command=win.destroy).pack(side="left", padx=10)
    
    def generate_default_logfile():
        if not files:
            return ""
        first = files[0]["html"]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return str(first.parent / f"html2pdf_{ts}_log.txt")

    def toggle_log_widgets():
        if log_enabled.get():
            log_button.config(state="normal")
            if not logfile_path.get():
                logfile_path.set(generate_default_logfile())
            log_label.config(text=logfile_path.get())
        else:
            log_button.config(state="disabled")
            log_label.config(text="")
            logfile_path.set("")

    def choose_logfile():
        initial = logfile_path.get() or generate_default_logfile()
        folder = Path(initial).parent
        filename = Path(initial).name

        path = filedialog.asksaveasfilename(
            title="Logdatei wählen",
            initialdir=str(folder),
            initialfile=filename,
            defaultextension=".txt",
            filetypes=[("Textdateien", "*.txt")]
        )
        if path:
            logfile_path.set(path)
            log_label.config(text=path)

    def make_relative(path: Path) -> str:
        try:
            rel = path.relative_to(current_root)
            rel_str = str(rel).replace("/", "\\")
            if rel_str == "" or rel_str == ".":
                return ".\\"
            return f".\\{rel_str}\\"
        except ValueError:
            # Pfad liegt außerhalb des Arbeitsordners → absolut
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
            "- Protokollierung ist in der GUI optional verfügbar.\n"
        )
        messagebox.showinfo("Information", msg)

    def request_cancel():
        nonlocal cancel_requested, current_process
        cancel_requested = True
        status_var.set("Abbruch angefordert…")

        if current_process and current_process.poll() is None:
            try:
                current_process.send_signal(signal.CTRL_BREAK_EVENT)
            except Exception:
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

        # Logger vorbereiten
        gui_logger = None
        if log_enabled.get():

            # Falls kein Pfad gesetzt → automatisch erzeugen
            if not logfile_path.get():

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                if files:
                    # Ordner der ersten Datei
                    first = files[0]["html"]
                    logfile_path.set(str(first.parent / f"html2pdf_{ts}_log.txt"))
                else:
                    # Fallback: aktueller Arbeitsordner
                    logfile_path.set(str(current_root / f"html2pdf_{ts}_log.txt"))

                # GUI aktualisieren
                log_label.config(text=logfile_path.get())

            gui_logger = GuiLogger(Path(logfile_path.get()))


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

                process = start_wkhtmltopdf(html_path, pdf_path)
                current_process = process

                def read_stderr(proc):
                    for line in proc.stderr:
                        line = line.strip()
                        if line:
                            app.after_idle(lambda l=line: status_var.set(l))

                threading.Thread(target=read_stderr, args=(process,), daemon=True).start()

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

                code, stdout, stderr = run_and_wait(process)

                if code != 0:
                    entry["status"] = "Fehler: Unbekannter Fehler"
                else:
                    entry["status"] = "Fertig ✔"

                # Logging
                if gui_logger:
                    gui_logger.add_entry(html_path, pdf_path, entry["status"])

                if idx % 20 == 0:
                    app.after_idle(refresh_tree)

                if idx % 10 == 0:
                    app.after_idle(lambda i=idx: status_var.set(f"Verarbeitet: {i+1}/{total}"))

            def finish():
                progress.stop()
                progress.config(mode="determinate")
                progress["value"] = progress["maximum"]


                if gui_logger:
                    gui_logger.write_log()

                    if messagebox.askyesno(
                        "Protokoll erstellt",
                        "Die Konvertierung ist abgeschlossen.\n"
                        "Es wurde eine Protokolldatei erstellt.\n\n"
                        "Möchten Sie die Protokolldatei jetzt ansehen?"
                    ):
                        show_logfile_window(logfile_path.get())



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

    exit_button = ttk.Button(top_frame, text="❎ Beenden", command=request_exit)
    exit_button.pack(side="right")

    ttk.Button(top_frame, text="ℹ️ INFO", command=show_info).pack(side="right", padx=(0, 5))

    # -----------------------------------------------------
    # Logging-Zeile direkt unterhalb der oberen Buttons
    # -----------------------------------------------------
    log_frame = ttk.Frame(main_frame)
    log_frame.pack(fill="x", pady=(5, 5))

    log_check = ttk.Checkbutton(
        log_frame,
        text="📝 Protokoll",
        variable=log_enabled,
        command=lambda: toggle_log_widgets()
    )
    log_check.pack(side="left")

    log_button = ttk.Button(
        log_frame,
        text="Logdatei wählen…",
        command=lambda: choose_logfile(),
        state="disabled"
    )
    log_button.pack(side="left", padx=(10, 0))

    log_label = ttk.Label(log_frame, text="", foreground="gray")
    log_label.pack(side="left", padx=(10, 0))

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
    # Fenster schließen abfangen
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