import tkinter as tk
import calendar
from datetime import datetime

MONTH_NAMES = [
    "Thang 1", "Thang 2", "Thang 3", "Thang 4",
    "Thang 5", "Thang 6", "Thang 7", "Thang 8",
    "Thang 9", "Thang 10", "Thang 11", "Thang 12",
]
WEEKDAYS = ["Thu 2", "Thu 3", "Thu 4", "Thu 5", "Thu 6", "Thu 7", "CN"]

LIGHT_THEME = {
    "bg": "#f5f5f5",
    "header_bg": "#2c3e50",
    "text": "#2c3e50",
    "form_bg": "#ecf0f1",
    "selected_text": "#2980b9",
    "weekday_bg": "#34495e",
    "cal_bg": "#ffffff",
    "day_text": "#2c3e50",
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "header_bg": "#0d47a1",
    "text": "#ffffff",
    "form_bg": "#2d2d2d",
    "selected_text": "#64b5f6",
    "weekday_bg": "#1565c0",
    "cal_bg": "#2d2d2d",
    "day_text": "#ffffff",
}

def open_calendar(dark_mode=False):
    theme = DARK_THEME if dark_mode else LIGHT_THEME
    
    win = tk.Toplevel()
    win.title("Lich")
    win.geometry("580x500")
    win.resizable(False, False)
    win.configure(bg=theme["bg"])

    header = tk.Label(win, text="Lich hien tai", font=("Arial", 16, "bold"), bg=theme["header_bg"], fg="white")
    header.pack(fill=tk.X, pady=0)

    today = datetime.now()
    selected_year = tk.IntVar(value=today.year)
    selected_month = tk.IntVar(value=today.month)
    firstweekday = tk.IntVar(value=0)
    date_format = tk.StringVar(value="%d/%m/%Y")
    selected_date = tk.StringVar(value="Chon mot ngay...")

    main_frame = tk.Frame(win, bg=theme["bg"])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    config_frame = tk.LabelFrame(main_frame, text="Cau hinh", font=("Arial", 10, "bold"), bg=theme["form_bg"], fg=theme["text"])
    config_frame.pack(fill=tk.X, pady=8)

    tk.Label(config_frame, text="Nam:", font=("Arial", 9), bg=theme["form_bg"], fg=theme["text"]).grid(row=0, column=0, sticky="w", padx=8, pady=5)
    year_menu = tk.OptionMenu(config_frame, selected_year, *range(today.year - 2, today.year + 6))
    year_menu.config(bg="white", width=8, fg="#000")
    year_menu.grid(row=0, column=1, sticky="w", padx=5)

    tk.Label(config_frame, text="Thang:", font=("Arial", 9), bg=theme["form_bg"], fg=theme["text"]).grid(row=0, column=2, sticky="w", padx=8)
    month_menu = tk.OptionMenu(config_frame, selected_month, *range(1, 13))
    month_menu.config(bg="white", width=8, fg="#000")
    month_menu.grid(row=0, column=3, sticky="w", padx=5)

    tk.Label(config_frame, text="Tuan bat dau:", font=("Arial", 9), bg=theme["form_bg"], fg=theme["text"]).grid(row=1, column=0, sticky="w", padx=8, pady=5)
    weekday_menu = tk.OptionMenu(config_frame, firstweekday, 0, 6, command=lambda _: render_calendar())
    weekday_menu.config(bg="white", width=8, fg="#000")
    weekday_menu.grid(row=1, column=1, sticky="w", padx=5)

    tk.Label(config_frame, text="Dinh dang:", font=("Arial", 9), bg=theme["form_bg"], fg=theme["text"]).grid(row=1, column=2, sticky="w", padx=8)
    fmt_entry = tk.Entry(config_frame, textvariable=date_format, width=12, bg="white", fg="#000")
    fmt_entry.grid(row=1, column=3, sticky="w", padx=5)
    tk.Button(config_frame, text="Cap nhat", command=lambda: render_calendar(), bg="#3498db", fg="white", font=("Arial", 9), relief=tk.FLAT, padx=8, pady=3).grid(row=1, column=4, padx=8, pady=5)

    selected_label = tk.Label(main_frame, textvariable=selected_date, font=("Arial", 11, "bold"), fg=theme["selected_text"], bg=theme["bg"])
    selected_label.pack(pady=8)

    calendar_frame = tk.Frame(main_frame, bg=theme["cal_bg"], relief=tk.FLAT, bd=0)
    calendar_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    weekday_frame = tk.Frame(calendar_frame, bg=theme["weekday_bg"], height=30)
    weekday_frame.pack(fill=tk.X)
    for idx, name in enumerate(WEEKDAYS):
        tk.Label(weekday_frame, text=name, width=8, font=("Arial", 9, "bold"), fg="white", bg=theme["weekday_bg"]).grid(row=0, column=idx, padx=1, pady=4)

    days_frame = tk.Frame(calendar_frame, bg=theme["form_bg"])
    days_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    def select_day(day):
        dt = datetime(selected_year.get(), selected_month.get(), day)
        selected_date.set("Ban chon: " + dt.strftime(date_format.get()))

    def render_calendar():
        for widget in days_frame.winfo_children():
            widget.destroy()
        cal = calendar.Calendar(firstweekday=firstweekday.get())
        weeks = cal.monthdayscalendar(selected_year.get(), selected_month.get())
        for row, week in enumerate(weeks):
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(days_frame, text="", width=8, height=3, bg=theme["form_bg"]).grid(row=row, column=col, padx=1, pady=2)
                else:
                    btn = tk.Button(days_frame, text=str(day), width=8, height=3, font=("Arial", 10), fg=theme["day_text"], bg=theme["form_bg"], relief=tk.RAISED, command=lambda d=day: select_day(d))
                    if (selected_year.get(), selected_month.get(), day) == (today.year, today.month, today.day):
                        btn.config(bg="#3498db", fg="white", font=("Arial", 10, "bold"))
                    btn.grid(row=row, column=col, padx=1, pady=2, sticky="nsew")
                days_frame.grid_rowconfigure(row, weight=1)
                days_frame.grid_columnconfigure(col, weight=1)

    def update_month(*_):
        render_calendar()

    selected_year.trace_add("write", update_month)
    selected_month.trace_add("write", update_month)
    render_calendar()
