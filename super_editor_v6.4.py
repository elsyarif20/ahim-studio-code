import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, subprocess, sys, threading

# ==========================================================
# AHIM STUDIO CODE v6.4 — Editor Modern Serbaguna
# ==========================================================

APP_NAME = "Ahim Studio Code"
APP_VERSION = "6.4"
DIST_PATH = os.path.join(os.getcwd(), "dist")
ICON_PATH = os.path.join(os.getcwd(), "icon.ico")

os.makedirs(DIST_PATH, exist_ok=True)

class AhimStudioCode(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1200x700")
        self.configure(bg="white")
        self.iconbitmap(ICON_PATH)

        # Warna Tema
        self.colors = {
            "bg": "white",
            "fg": "black",
            "accent": "#16a34a",      # Hijau cerah
            "border": "#002b5b",      # Biru gelap
        }

        # Layout utama
        self.create_topbar()
        self.create_sidebar()
        self.create_main_area()

    # ==========================================================
    # Bagian: UI
    # ==========================================================
    def create_topbar(self):
        topbar = tk.Frame(self, bg=self.colors["border"], height=40)
        topbar.pack(fill="x", side="top")

        tk.Label(topbar, text="🟩 Ahim Studio Code", bg=self.colors["border"],
                 fg="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10)

        tk.Button(topbar, text="Run ▶", bg=self.colors["accent"], fg="white",
                  font=("Segoe UI", 10, "bold"), command=self.run_code).pack(side="right", padx=10, pady=5)

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg=self.colors["border"], width=180)
        sidebar.pack(fill="y", side="left")

        buttons = [
            ("📝 Notepad", self.show_notepad),
            ("💻 Terminal", self.show_terminal),
            ("📁 File Manager", self.show_file_manager),
            ("📦 Library", self.show_library),
            ("⚙️ Dependensi", self.show_dependensi),
            ("🚀 Build Tools", self.show_build_tools),
        ]

        for text, cmd in buttons:
            tk.Button(sidebar, text=text, bg=self.colors["accent"], fg="white",
                      relief="flat", font=("Segoe UI", 10, "bold"),
                      command=cmd, height=2).pack(fill="x", pady=2, padx=4)

    def create_main_area(self):
        self.main_frame = tk.Frame(self, bg=self.colors["bg"])
        self.main_frame.pack(fill="both", expand=True)
        self.show_notepad()

    # ==========================================================
    # Panel: NOTEPAD
    # ==========================================================
    def show_notepad(self):
        self.clear_main()
        frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        frame.pack(fill="both", expand=True)

        self.text_area = tk.Text(frame, wrap="none", undo=True, font=("Consolas", 12),
                                 bg="white", fg="black", insertbackground="black")
        self.text_area.pack(fill="both", expand=True, padx=(40, 0), pady=5)

        # Line number di luar text
        self.line_numbers = tk.Text(frame, width=4, bg="#f0f0f0", fg="gray",
                                    font=("Consolas", 10), state="disabled", wrap="none")
        self.line_numbers.pack(side="left", fill="y")
        self.update_line_numbers()

        self.text_area.bind("<KeyRelease>", lambda e: self.update_line_numbers())

    def update_line_numbers(self):
        lines = self.text_area.get("1.0", "end-1c").split("\n")
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        for i in range(1, len(lines) + 1):
            self.line_numbers.insert("end", f"{i}\n")
        self.line_numbers.config(state="disabled")

    # ==========================================================
    # Panel: TERMINAL
    # ==========================================================
    def show_terminal(self):
        self.clear_main()
        frame = tk.Frame(self.main_frame, bg="black")
        frame.pack(fill="both", expand=True)
        self.terminal_output = tk.Text(frame, bg="black", fg="lime", font=("Consolas", 11))
        self.terminal_output.pack(fill="both", expand=True)
        threading.Thread(target=self.run_terminal, daemon=True).start()

    def run_terminal(self):
        self.terminal_output.insert("end", "Terminal aktif...\nKetik perintah di sini belum diaktifkan.\n")

    # ==========================================================
    # Panel: FILE MANAGER
    # ==========================================================
    def show_file_manager(self):
        self.clear_main()
        frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        frame.pack(fill="both", expand=True)
        path_label = tk.Label(frame, text="Pilih Folder:", bg="white", fg="black")
        path_label.pack(pady=5)
        path = filedialog.askdirectory()
        if path:
            for f in os.listdir(path):
                tk.Label(frame, text=f"📄 {f}", bg="white", anchor="w").pack(fill="x")

    # ==========================================================
    # Panel: LIBRARY
    # ==========================================================
    def show_library(self):
        self.clear_main()
        frame = tk.Frame(self.main_frame, bg="white")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Instal Library (pip):", bg="white", font=("Segoe UI", 11, "bold")).pack(pady=10)
        entry = tk.Entry(frame, width=40, font=("Consolas", 11))
        entry.pack(pady=5)

        def install_lib():
            pkg = entry.get()
            if pkg:
                messagebox.showinfo("Menginstal", f"Menginstal {pkg}...")
                threading.Thread(target=lambda: subprocess.run([sys.executable, "-m", "pip", "install", pkg])).start()

        tk.Button(frame, text="Install", bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  command=install_lib).pack(pady=10)

    # ==========================================================
    # Panel: DEPENDENSI
    # ==========================================================
    def show_dependensi(self):
        self.clear_main()
        frame = tk.Frame(self.main_frame, bg="white")
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Dependensi Project:", bg="white", font=("Segoe UI", 11, "bold")).pack(pady=10)

        tk.Label(frame, text="1️⃣ pyinstaller\n2️⃣ inno setup\n3️⃣ WiX Toolset", bg="white", justify="left").pack(pady=10)

    # ==========================================================
    # Panel: BUILD TOOLS
    # ==========================================================
    def show_build_tools(self):
        self.clear_main()
        frame = tk.Frame(self.main_frame, bg="white")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="🚀 Build Tools", bg="white", font=("Segoe UI", 12, "bold")).pack(pady=10)

        tk.Button(frame, text="Build .EXE", bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  command=self.build_exe).pack(pady=5)
        tk.Button(frame, text="Generate .ISS (Inno)", bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  command=self.generate_iss).pack(pady=5)
        tk.Button(frame, text="Build .MSI (WiX)", bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  command=self.build_msi).pack(pady=5)

    # ==========================================================
    # Fungsi build
    # ==========================================================
    def build_exe(self):
        subprocess.run(["pyinstaller", "--noconfirm", "--onefile", "main.py", "--icon", ICON_PATH, "--distpath", DIST_PATH])
        messagebox.showinfo("Selesai", "Build .EXE selesai!")

    def generate_iss(self):
        iss_path = os.path.join(DIST_PATH, "Ahim_Studio_Code.iss")
        with open(iss_path, "w", encoding="utf-8") as f:
            f.write(self.make_iss_template())
        messagebox.showinfo("Selesai", f"File .ISS dibuat di:\n{iss_path}")

    def build_msi(self):
        subprocess.run(["pyinstaller", "--onefile", "main.py", "--distpath", DIST_PATH])
        messagebox.showinfo("Info", "Gunakan WiX Toolset untuk compile menjadi .msi")

    def make_iss_template(self):
        return f"""[Setup]
AppName=Ahim Studio Code
AppVersion={APP_VERSION}
DefaultDirName={{pf}}\\Ahim Studio Code
DefaultGroupName=Ahim Studio Code
OutputDir={DIST_PATH}
OutputBaseFilename=Ahim_Studio_Code
SetupIconFile={ICON_PATH}
Compression=lzma
SolidCompression=yes

[Files]
Source: "{DIST_PATH}\\Ahim_Studio_Code.exe"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{autoprograms}}\\Ahim Studio Code"; Filename: "{{app}}\\Ahim_Studio_Code.exe"
Name: "{{autodesktop}}\\Ahim Studio Code"; Filename: "{{app}}\\Ahim_Studio_Code.exe"

[Run]
Filename: "{{app}}\\Ahim_Studio_Code.exe"; Description: "Jalankan Ahim Studio Code"; Flags: nowait postinstall skipifsilent
"""

    def run_code(self):
        code = self.text_area.get("1.0", "end-1c")
        temp_file = "temp_run.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)
        subprocess.run(["python", temp_file])

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = AhimStudioCode()
    app.mainloop()
