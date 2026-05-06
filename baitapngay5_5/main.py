import tkinter as tk
from clock_form import open_clock
from calendar_form import open_calendar
from reminder_form import open_reminder

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ung dung thoi gian")
        self.root.geometry("400x420")
        self.root.resizable(False, False)
        
        self.dark_mode = tk.BooleanVar(value=False)
        self.apply_theme()
        
        self.setup_ui()
    
    def apply_theme(self):
        if self.dark_mode.get():
            self.bg_color = "#1e1e1e"
            self.header_bg = "#0d47a1"
            self.text_color = "#ffffff"
            self.label_color = "#b0b0b0"
            self.frame_bg = "#2d2d2d"
        else:
            self.bg_color = "#f5f5f5"
            self.header_bg = "#2c3e50"
            self.text_color = "#2c3e50"
            self.label_color = "#7f8c8d"
            self.frame_bg = "#ecf0f1"
        
        self.root.configure(bg=self.bg_color)
    
    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.apply_theme()
        self.setup_ui()
    
    def open_clock_wrapper(self):
        open_clock(dark_mode=self.dark_mode.get())
    
    def open_calendar_wrapper(self):
        open_calendar(dark_mode=self.dark_mode.get())
    
    def open_reminder_wrapper(self):
        open_reminder(dark_mode=self.dark_mode.get())
    
    def setup_ui(self):
        header = tk.Label(self.root, text="Ung dung thoi gian", font=("Arial", 18, "bold"), bg=self.header_bg, fg="white")
        header.pack(fill=tk.X, pady=0)
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_label = tk.Label(main_frame, text="Chon mot chuc nang", font=("Arial", 12, "bold"), fg=self.text_color, bg=self.bg_color)
        title_label.pack(pady=10)
        
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=15)
        
        btn_style = {"font": ("Arial", 11, "bold"), "width": 24, "height": 2, "relief": tk.FLAT, "cursor": "hand2"}
        
        tk.Button(button_frame, text="Dong ho", command=self.open_clock_wrapper, bg="#3498db", fg="white", **btn_style).pack(pady=6)
        tk.Button(button_frame, text="Lich", command=self.open_calendar_wrapper, bg="#2ecc71", fg="white", **btn_style).pack(pady=6)
        tk.Button(button_frame, text="Nhac viec", command=self.open_reminder_wrapper, bg="#e74c3c", fg="white", **btn_style).pack(pady=6)
        
        theme_frame = tk.Frame(main_frame, bg=self.frame_bg)
        theme_frame.pack(fill=tk.X, pady=10, padx=10)
        
        theme_check = tk.Checkbutton(theme_frame, text="Dark Mode", variable=self.dark_mode, command=self.refresh_ui, bg=self.frame_bg, fg=self.text_color, font=("Arial", 10), activebackground=self.frame_bg, activeforeground=self.text_color, selectcolor=self.frame_bg)
        theme_check.pack(padx=8, pady=6)
        
        footer = tk.Label(main_frame, text="Quan ly thoi gian, lich va nhac nho", wraplength=340, justify="center", fg=self.label_color, bg=self.bg_color, font=("Arial", 9))
        footer.pack(pady=10)

root = tk.Tk()
app = App(root)

try:
    root.mainloop()
except KeyboardInterrupt:
    root.quit()
