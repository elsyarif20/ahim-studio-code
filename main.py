import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading

class AhimStudioCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Ahim Studio Code v6.4")
        self.root.geometry("1200x700")
        self.root.configure(bg="white")

        # === Theme colors ===
        self.green = "#00C853"   # bright green
        self.blue = "#0D47A1"    # dark blue border
        self.white = "#FFFFFF"

        # === Menu Bar ===
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Build EXE", command=self.build_exe)
        tools_menu.add_command(label="Build ISS", command=self.build_iss)
        tools_menu.add_command(label="Build MSI", command=self.build_msi)
        menubar.add_cascade(label="Build", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menubar)

        # === Top Toolbar Buttons ===
        toolbar = tk.Frame(root, bg=self.white, height=40, relief="solid", bd=2)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        buttons = [
            ("📝 Notepad", self.show_notepad),
            ("💻 Terminal", self.show_terminal),
            ("📁 File Manager", self.show_file_manager),
            ("📦 Library", self.show_library),
            ("⚙️ Dependensi", self.show_dependensi)
        ]

        for (text, cmd) in buttons:
            ttk.Button(toolbar, text=text, command=cmd).pack(side=tk.LEFT, padx=5, pady=5)

        # === Status Bar ===
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=self.white)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # === Main Area ===
        self.main_frame = tk.Frame(root, bg=self.white, relief="solid", bd=2)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # === Default View ===
        self.show_notepad()

    # ===============================
    # 🔹 Notepad View
    # ===============================
    def show_notepad(self):
        self.clear_main()
        self.status_var.set("Notepad siap digunakan")

        # Line numbers
        line_frame = tk.Frame(self.main_frame, width=40, bg=self.blue)
        line_frame.pack(side=tk.LEFT, fill=tk.Y)
        text_area = scrolledtext.ScrolledText(self.main_frame, undo=True, wrap="none", font=("Consolas", 12))
        text_area.pack(fill=tk.BOTH, expand=True)

        # Update line numbers
        def update_lines(event=None):
            lines = "\n".join(str(i) for i in range(1, int(text_area.index('end').split('.')[0])))
            for widget in line_frame.winfo_children():
                widget.destroy()
            tk.Label(line_frame, text=lines, justify="right", bg=self.blue, fg=self.white, font=("Consolas", 10)).pack(anchor="nw")

        text_area.bind("<KeyRelease>", update_lines)
        update_lines()

        self.text_area = text_area

    # ===============================
    # 🔹 Terminal View
    # ===============================
    def show_terminal(self):
        self.clear_main()
        self.status_var.set("Terminal aktif")

        frame = tk.Frame(self.main_frame, bg=self.white)
        frame.pack(fill=tk.BOTH, expand=True)

        output = scrolledtext.ScrolledText(frame, state="disabled", bg="black", fg="lime", font=("Consolas", 11))
        output.pack(fill=tk.BOTH, expand=True)

        entry = tk.Entry(frame, bg=self.white, fg="black", font=("Consolas", 11))
        entry.pack(fill=tk.X)

        def run_cmd(event=None):
            cmd = entry.get()
            entry.delete(0, tk.END)

            def execute():
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    output.config(state="normal")
                    output.insert(tk.END, f"> {cmd}\n{result.stdout}\n{result.stderr}\n")
                    output.config(state="disabled")
                    output.see(tk.END)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            threading.Thread(target=execute).start()

        entry.bind("<Return>", run_cmd)

    # ===============================
    # 🔹 File Manager
    # ===============================
    def show_file_manager(self):
        self.clear_main()
        self.status_var.set("File Manager siap digunakan")

        tree = ttk.Treeview(self.main_frame)
        tree.pack(fill=tk.BOTH, expand=True)

        drive = os.getcwd()
        root_node = tree.insert("", "end", text=drive, open=True)

        def populate(node, path):
            try:
                for p in os.listdir(path):
                    abspath = os.path.join(path, p)
                    oid = tree.insert(node, "end", text=p, open=False)
                    if os.path.isdir(abspath):
                        tree.insert(oid, "end")
            except PermissionError:
                pass

        def update_tree(event):
            node = tree.focus()
            path = self.get_full_path(tree, node)
            children = tree.get_children(node)
            if children:
                for c in children:
                    tree.delete(c)
            populate(node, path)

        tree.bind("<<TreeviewOpen>>", update_tree)
        populate(root_node, drive)

    def get_full_path(self, tree, node):
        path = tree.item(node)["text"]
        parent = tree.parent(node)
        while parent:
            path = os.path.join(tree.item(parent)["text"], path)
            parent = tree.parent(parent)
        return path

    # ===============================
    # 🔹 Library Manager
    # ===============================
    def show_library(self):
        self.clear_main()
        self.status_var.set("Library Manager siap")

        frame = tk.Frame(self.main_frame, bg=self.white)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Install Library Python:", bg=self.white, fg=self.blue, font=("Arial", 12, "bold")).pack(anchor="w")

        entry = tk.Entry(frame, font=("Consolas", 12))
        entry.pack(fill=tk.X, pady=5)

        output = scrolledtext.ScrolledText(frame, height=15, font=("Consolas", 11))
        output.pack(fill=tk.BOTH, expand=True)

        def install_lib():
            lib = entry.get().strip()
            if not lib:
                return
            output.insert(tk.END, f"Installing {lib}...\n")
            threading.Thread(target=self._install_lib, args=(lib, output)).start()

        ttk.Button(frame, text="Install", command=install_lib).pack(anchor="e", pady=5)

    def _install_lib(self, lib, output):
        result = subprocess.run(f"py -m pip install {lib}", shell=True, capture_output=True, text=True)
        output.insert(tk.END, result.stdout + "\n" + result.stderr)

    # ===============================
    # 🔹 Dependensi Manager
    # ===============================
    def show_dependensi(self):
        self.clear_main()
        self.status_var.set("Dependensi Manager aktif")

        frame = tk.Frame(self.main_frame, bg=self.white)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Tambah dependensi proyek:", bg=self.white, fg=self.blue, font=("Arial", 12, "bold")).pack(anchor="w")

        dep_entry = tk.Entry(frame, font=("Consolas", 12))
        dep_entry.pack(fill=tk.X, pady=5)

        deps_box = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 11))
        deps_box.pack(fill=tk.BOTH, expand=True)

        def add_dep():
            dep = dep_entry.get().strip()
            if dep:
                deps_box.insert(tk.END, dep + "\n")
                dep_entry.delete(0, tk.END)

        ttk.Button(frame, text="Tambah", command=add_dep).pack(anchor="e", pady=5)

    # ===============================
    # 🔹 Utility Functions
    # ===============================
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("File baru dibuat")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())
            self.status_var.set(f"Membuka {path}")

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, tk.END))
            self.status_var.set(f"Disimpan ke {path}")

    def build_exe(self):
        messagebox.showinfo("Build EXE", "Building EXE... (pastikan PyInstaller terinstal)")
        subprocess.run("pyinstaller --onefile --noconsole --icon=icon.ico main.py -n Ahim_Studio_Code", shell=True)

    def build_iss(self):
        messagebox.showinfo("Build ISS", "Membuat file installer .iss...")
        subprocess.run("iscc build_tools\\build_iss.iss", shell=True)

    def build_msi(self):
        messagebox.showinfo("Build MSI", "Membuat MSI (via WiX)...")
        subprocess.run("build_tools\\build_msi.bat", shell=True)

    def show_about(self):
        messagebox.showinfo("Tentang", "Ahim Studio Code v6.4\nEditor modern buatan lokal.\n© 2025 Ahim Dev")

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AhimStudioCode(root)
    root.mainloop()
