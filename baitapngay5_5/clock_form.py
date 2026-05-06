import tkinter as tk
from datetime import datetime, timedelta, timezone

TIMEZONE_OFFSETS = {
    "UTC": 0,
    "Asia/Ho_Chi_Minh": 7,
    "Asia/Tokyo": 9,
    "Europe/London": 0,
    "America/New_York": -5,
    "Australia/Sydney": 10,
}
TIMEZONES = list(TIMEZONE_OFFSETS.keys())
TIME_FORMATS = {
    "24 gio": "%H:%M:%S",
    "12 gio": "%I:%M:%S %p",
}

LIGHT_THEME = {
    "bg": "#f5f5f5",
    "header_bg": "#2c3e50",
    "text": "#2c3e50",
    "text_light": "#555",
    "form_bg": "#ecf0f1",
    "label_color": "#7f8c8d",
    "time_color": "#2980b9",
    "sep_color": "#bdc3c7",
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "header_bg": "#0d47a1",
    "text": "#ffffff",
    "text_light": "#b0b0b0",
    "form_bg": "#2d2d2d",
    "label_color": "#90caf9",
    "time_color": "#64b5f6",
    "sep_color": "#424242",
}

def open_clock(dark_mode=False):
    theme = DARK_THEME if dark_mode else LIGHT_THEME
    
    win = tk.Toplevel()
    win.title("Dong ho")
    win.geometry("420x420")
    win.resizable(False, False)
    win.configure(bg=theme["bg"])

    header = tk.Label(win, text="Dong ho the gioi", font=("Times New Roman", 18, "bold"), bg=theme["header_bg"], fg="white")
    header.pack(fill=tk.X, pady=0)

    main_frame = tk.Frame(win, bg=theme["bg"])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

    local_label = tk.Label(main_frame, font=("Times New Roman", 34, "bold"), fg=theme["time_color"], bg=theme["bg"], justify="center")
    local_label.pack(pady=10)

    local_date_label = tk.Label(main_frame, font=("Times New Roman", 12), fg=theme["text_light"], bg=theme["bg"], justify="center")
    local_date_label.pack(pady=5)

    sep1 = tk.Frame(main_frame, height=1, bg=theme["sep_color"])
    sep1.pack(fill=tk.X, pady=5)

    tz_label = tk.Label(main_frame, font=("Arial", 11), fg=theme["label_color"], bg=theme["bg"], justify="center")
    tz_label.pack(pady=5)

    convert_label = tk.Label(main_frame, font=("Arial", 10), fg=theme["text_light"], bg=theme["bg"], justify="center")
    convert_label.pack(pady=3)

    sep2 = tk.Frame(main_frame, height=1, bg=theme["sep_color"])
    sep2.pack(fill=tk.X, pady=5)

    config_frame = tk.LabelFrame(main_frame, text="Cau hinh", font=("Times New Roman", 11, "bold"), bg=theme["form_bg"], fg=theme["text"])
    config_frame.pack(fill=tk.X, pady=10)

    tk.Label(config_frame, text="Mui gio:", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=0, column=0, sticky="w", padx=8, pady=5)
    selected_tz = tk.StringVar(value=TIMEZONES[0])
    tz_menu = tk.OptionMenu(config_frame, selected_tz, *TIMEZONES)
    tz_menu.config(bg="white", width=15, fg="#000")
    tz_menu.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    tk.Label(config_frame, text="Hoac nhap:", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=1, column=0, sticky="w", padx=8, pady=5)
    custom_tz = tk.Entry(config_frame, width=18, bg="white", fg="#000", font=("Times New Roman", 11))
    custom_tz.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    tk.Label(config_frame, text="Dinh dang:", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=2, column=0, sticky="w", padx=8, pady=5)
    selected_format = tk.StringVar(value="24 gio")
    fmt_menu = tk.OptionMenu(config_frame, selected_format, *TIME_FORMATS.keys())
    fmt_menu.config(bg="white", width=15, fg="#000")
    fmt_menu.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    show_date = tk.BooleanVar(value=True)
    date_check = tk.Checkbutton(config_frame, text="Hien thi ngay", variable=show_date, bg=theme["form_bg"], fg=theme["text"], activebackground=theme["form_bg"], activeforeground=theme["text"], selectcolor=theme["form_bg"], font=("Times New Roman", 11))
    date_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=8, pady=5)

    status_label = tk.Label(main_frame, text="", fg="#e74c3c", bg=theme["bg"], font=("Arial", 9))
    status_label.pack(pady=5)

    update_status = tk.Label(main_frame, text="Cap nhat moi giay...", fg=theme["label_color"], bg=theme["bg"], font=("Arial", 8))
    update_status.pack(pady=2)

    def get_timezone():
        tz_name = custom_tz.get().strip() or selected_tz.get()
        if tz_name in TIMEZONE_OFFSETS:
            return timezone(timedelta(hours=TIMEZONE_OFFSETS[tz_name])), tz_name
        status_label.config(text="Mui gio khong ho tro: %s. Hien thi gio dia phuong." % tz_name)
        return datetime.now().astimezone().tzinfo, "Dia phuong"

    def format_time(dt):
        return dt.strftime(TIME_FORMATS[selected_format.get()])

    def update_clock():
        now_local = datetime.now()
        local_label.config(text=format_time(now_local))
        local_date_label.config(text=now_local.strftime("%d/%m/%Y") if show_date.get() else "")

        tz, tz_name = get_timezone()
        tz_time = datetime.now(tz)
        tz_label.config(text="Gio mui %s: %s" % (tz_name, format_time(tz_time)))
        convert_label.config(text="Tuong ung dia phuong: %s" % tz_time.astimezone().strftime("%H:%M:%S %d/%m/%Y"))
        status_label.config(text="")
        update_status.config(text="Cap nhat: %s" % now_local.strftime("%H:%M:%S"))
        win.after(200, update_clock)

    update_clock()
