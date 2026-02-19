import os
import customtkinter as ctk
from gui.styles import PADDING, CORNER_RADIUS, FONTS, COLORS, Localizer, ThemeManager
from tkinter import messagebox
from pathlib import Path

class CTkFileExplorer(ctk.CTkToplevel):
    def __init__(self, master, title=None, file_types=[("All Files", "*.*")], initial_dir=None):
        super().__init__(master)
        
        # Localization
        self.title_text = title if title else Localizer.translate("select_file")
        self.title(self.title_text)
        self.geometry("900x600")
        
        # Path Handling - FIX: Proper expansion
        start_path = os.path.abspath(os.path.expanduser(initial_dir or "~"))
        self.current_path = start_path # Use string directly
        
        # Centering
        self.update_idletasks()
        width, height = 900, 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.lift()
        self.attributes("-topmost", True)
        self.after(50, self.grab_set)
        
        self.file_types = file_types
        self.selected_file = None
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # 1. Path Bar
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=PADDING, pady=10)
        self.top_frame.grid_columnconfigure(1, weight=1)
        
        self.back_btn = ctk.CTkButton(self.top_frame, text="⭠", width=40, font=("Arial", 20), command=self.go_back)
        self.back_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.path_entry = ctk.CTkEntry(self.top_frame, font=FONTS["small"])
        self.path_entry.grid(row=0, column=1, sticky="ew")
        self.path_entry.bind("<Return>", lambda e: self.navigate_to(self.path_entry.get()))
        
        self.refresh_btn = ctk.CTkButton(self.top_frame, text="↻", width=40, font=("Arial", 20), command=self.refresh)
        self.refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # 2. List Area
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=ThemeManager.get_tuple("bg"), corner_radius=CORNER_RADIUS)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=PADDING, pady=5)
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        # 3. Bottom Bar
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=PADDING, pady=10)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        self.file_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text=Localizer.translate("filename"))
        self.file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.type_menu = ctk.CTkOptionMenu(self.bottom_frame, values=[t[0] for t in file_types], width=180)
        self.type_menu.grid(row=0, column=1, padx=(0, 10))
        self.type_menu.configure(command=lambda _: self.update_list())
        
        self.cancel_btn = ctk.CTkButton(self.bottom_frame, text=Localizer.translate("cancel_btn"), 
                                        fg_color="transparent", border_width=1, command=self.close)
        self.cancel_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.select_btn = ctk.CTkButton(self.bottom_frame, text=Localizer.translate("open"), command=self.on_select)
        self.select_btn.grid(row=0, column=3)
        
        # Initial Load
        self._rows = []
        self.after(100, self.update_list)

    def update_path_entry(self):
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, str(self.current_path))

    def update_list(self):
        """Standardized and ultra-robust directory listing."""
        for r in self._rows:
            try: r.destroy()
            except: pass
        self._rows = []
        
        try:
            curr = os.path.abspath(str(self.current_path))
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, curr)

            parent = os.path.dirname(curr)
            if parent != curr:
                self.add_row("..", True, parent)

            try:
                names = os.listdir(curr)
            except Exception as e:
                messagebox.showwarning("Hata", f"Erisim Hatasi: {e}")
                return

            try:
                sel = self.type_menu.get()
                info = [t for t in self.file_types if t[0] == sel]
                f_str = info[0][1].lower() if info else "*.*"
            except:
                f_str = "*.*"
            
            exts = [x.strip("*").lower() for x in f_str.replace(";", " ").split() if x.strip("*")]
            all_f = "*.*" in f_str or not exts

            dirs, files = [], []
            for n in names:
                try:
                    full = os.path.join(curr, n)
                    if os.path.isdir(full): dirs.append(n)
                    else:
                        if all_f or any(n.lower().endswith(e) for e in exts): files.append(n)
                except: continue

            dirs.sort(key=str.lower)
            files.sort(key=str.lower)

            # 7. Title Update (Minimalist)
            self.title(f"{self.title_text} - {os.path.basename(curr) or curr}")

            for d in dirs: self.add_row(d, True, os.path.join(curr, d))
            for f in files: self.add_row(f, False, os.path.join(curr, f))

            if not self._rows:
                self.show_error("Klasör boş veya filtreye uygun dosya yok.")
                
            self.list_frame.update_idletasks()
            self.after(50, self._ens_top)
        except Exception as ex:
            messagebox.showwarning("Hata", f"Sistem Hatasi: {ex}")

    def _ens_top(self):
        try:
            c = getattr(self.list_frame, "_parent_canvas", None) or getattr(self.list_frame, "_canvas", None)
            if c: c.yview_moveto(0)
        except: pass

    def show_error(self, msg):
        l = ctk.CTkLabel(self.list_frame, text=msg, font=FONTS["body"], 
                         text_color=ThemeManager.get_tuple("error"), pady=50)
        l.pack(fill="x")
        self._rows.append(l)

    def add_row(self, name, is_dir, p_str):
        row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        row.pack(fill="x", pady=1, padx=2)
        self._rows.append(row)
        
        icon = "📁" if is_dir or name == ".." else "📄"
        btn = ctk.CTkButton(
            row, text=f"  {icon}   {name}", 
            anchor="w", fg_color="transparent", 
            text_color=ThemeManager.get_tuple("text"),
            hover_color=ThemeManager.get_tuple("card_hover"),
            command=lambda p=p_str, d=is_dir: self.on_click(p, d),
            height=34, corner_radius=0
        )
        btn.pack(fill="x")
        
        def _swheel(e):
            c = getattr(self.list_frame, "_parent_canvas", None) or getattr(self.list_frame, "_canvas", None)
            if c:
                if e.num == 4: c.yview_scroll(-3, "units")
                elif e.num == 5: c.yview_scroll(3, "units")
                elif e.delta: c.yview_scroll(int(-1*(e.delta/120)), "units")

        btn.bind("<Button-4>", _swheel)
        btn.bind("<Button-5>", _swheel)
        btn.bind("<MouseWheel>", _swheel)

    def on_click(self, p_str, is_dir):
        if is_dir:
            self.current_path = p_str
            self.update_list()
            self.file_entry.delete(0, "end")
        else:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, os.path.basename(p_str))
            self.selected_file = p_str
            # Auto-select and close on single click
            self.on_select()

    def go_back(self):
        c = os.path.abspath(str(self.current_path))
        p = os.path.dirname(c)
        if p != c:
            self.current_path = p
            self.update_list()

    def navigate_to(self, s):
        try:
            exp = os.path.abspath(os.path.expanduser(s))
            if os.path.isdir(exp):
                self.current_path = exp
                self.update_list()
            else: messagebox.showerror("Hata", f"Yol bulunamadi: {s}")
        except: messagebox.showerror("Hata", "Gecersiz yol.")

    def refresh(self): self.update_list()

    def on_select(self):
        f = self.file_entry.get().strip()
        if f:
            t = f if os.path.isabs(f) else os.path.join(os.path.abspath(str(self.current_path)), f)
            if os.path.isfile(t):
                self.selected_file = t
                self.close()
            else: messagebox.showwarning("Uyarı", "Gecerli bir dosya degil.")
        else: messagebox.showwarning("Uyarı", "Lutfen bir dosya secin.")

    def close(self):
        self.grab_release()
        self.destroy()

    def get_result(self):
        self.master.wait_window(self)
        return self.selected_file
