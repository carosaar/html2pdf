"""
GUI-Frontend (Tkinter).
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from html2pdf.core.wkhtmltopdf_check import ensure_wkhtmltopdf_or_raise
from html2pdf.version import __version__

def run_gui():
    app = tk.Tk()
    app.title(f"html2pdf - HTML → PDF Converter (v{__version__})")

    file_list = []

    def select_files():
        paths = filedialog.askopenfilenames(filetypes=[("HTML Dateien", "*.html")])
        for p in paths:
            file_list.append(p)
            listbox.insert(tk.END, p)

    def start_conversion():
        try:
            ensure_wkhtmltopdf_or_raise()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            return

        if not file_list:
            messagebox.showwarning("Hinweis", "Keine Dateien ausgewählt.")
            return

        progress["maximum"] = len(file_list)

        def worker():
            for i, f in enumerate(file_list, start=1):
                progress["value"] = i
                status.set(f"Konvertiere: {f}")
                app.update_idletasks()
                # später: convert_single_html(...)
            status.set("Fertig.")

        threading.Thread(target=worker).start()

    frame = ttk.Frame(app, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Button(frame, text="HTML-Dateien auswählen", command=select_files).pack()

    listbox = tk.Listbox(frame, height=8)
    listbox.pack(fill="both", expand=True)

    progress = ttk.Progressbar(frame)
    progress.pack(fill="x", pady=5)

    status = tk.StringVar(value="Bereit.")
    ttk.Label(frame, textvariable=status).pack()

    ttk.Button(frame, text="Konvertieren", command=start_conversion).pack(pady=5)

    app.mainloop()
