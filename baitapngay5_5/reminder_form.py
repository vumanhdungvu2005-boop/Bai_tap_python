import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os

try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

REMINDERS_FILE = "reminders.json"

LIGHT_THEME = {
    "bg": "#f5f5f5",
    "header_bg": "#2c3e50",
    "text": "#2c3e50",
    "form_bg": "#ecf0f1",
    "listbox_bg": "#ffffff",
    "label_color": "#7f8c8d",
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "header_bg": "#0d47a1",
    "text": "#ffffff",
    "form_bg": "#2d2d2d",
    "listbox_bg": "#3d3d3d",
    "label_color": "#90caf9",
}

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                reminders = []
                for item in data:
                    reminders.append({
                        "title": item["title"],
                        "time": datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S"),
                        "offset": item["offset"],
                        "sent": item.get("sent", False),
                    })
                return reminders
        except Exception as e:
            print("Loi tai file JSON: %s" % e)
    return []

def save_reminders(reminders):
    try:
        data = []
        for item in reminders:
            data.append({
                "title": item["title"],
                "time": item["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "offset": item["offset"],
                "sent": item["sent"],
            })
        with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Loi luu JSON: %s" % e)

def open_reminder(dark_mode=False):
    theme = DARK_THEME if dark_mode else LIGHT_THEME
    
    win = tk.Toplevel()
    win.title("Nhac viec")
    win.geometry("550x580")
    win.resizable(False, False)
    win.configure(bg=theme["bg"])

    header = tk.Label(win, text="Quan ly nhac viec", font=("Times New Roman", 18, "bold"), bg=theme["header_bg"], fg="white")
    header.pack(fill=tk.X, pady=0)

    main_frame = tk.Frame(win, bg=theme["bg"])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    form_frame = tk.LabelFrame(main_frame, text="Nhap thong tin nhac", font=("Times New Roman", 12, "bold"), bg=theme["form_bg"], fg=theme["text"])
    form_frame.pack(fill=tk.X, pady=8)

    tk.Label(form_frame, text="Tieu de:", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=0, column=0, sticky="w", padx=8, pady=6)
    title_entry = tk.Entry(form_frame, width=35, bg="white", font=("Times New Roman", 11), fg="#000")
    title_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=6)

    tk.Label(form_frame, text="Ngay (dd/mm/yyyy):", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=1, column=0, sticky="w", padx=8, pady=6)
    date_entry = tk.Entry(form_frame, width=18, bg="white", font=("Times New Roman", 11), fg="#000")
    date_entry.grid(row=1, column=1, sticky="w", padx=8, pady=6)
    date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    tk.Label(form_frame, text="Gio (HH:MM):", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=2, column=0, sticky="w", padx=8, pady=6)
    time_entry = tk.Entry(form_frame, width=18, bg="white", font=("Times New Roman", 11), fg="#000")
    time_entry.grid(row=2, column=1, sticky="w", padx=8, pady=6)
    time_entry.insert(0, datetime.now().strftime("%H:%M"))

    tk.Label(form_frame, text="Nhac truoc (phut):", font=("Times New Roman", 11), bg=theme["form_bg"], fg=theme["text"]).grid(row=3, column=0, sticky="w", padx=8, pady=6)
    offset_entry = tk.Entry(form_frame, width=18, bg="white", font=("Times New Roman", 11), fg="#000")
    offset_entry.grid(row=3, column=1, sticky="w", padx=8, pady=6)
    offset_entry.insert(0, "0")

    form_frame.columnconfigure(1, weight=1)

    list_label = tk.Label(main_frame, text="Danh sach nhac viec (tu dong luu)", font=("Times New Roman", 12, "bold"), fg=theme["text"], bg=theme["bg"])
    list_label.pack(anchor="w", pady=(10, 4))

    reminder_list = tk.Listbox(main_frame, width=72, height=9, bg=theme["listbox_bg"], font=("Times New Roman", 10), fg=theme["text"], selectmode=tk.SINGLE, relief=tk.SUNKEN, bd=1)
    reminder_list.pack(fill=tk.BOTH, expand=True, pady=5)

    scrollbar = tk.Scrollbar(reminder_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    reminder_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=reminder_list.yview)

    status_label = tk.Label(main_frame, text="Tai tu file JSON...", fg=theme["label_color"], bg=theme["bg"], font=("Times New Roman", 10))
    status_label.pack(pady=5)

    sound_enabled = tk.BooleanVar(value=SOUND_AVAILABLE)
    if SOUND_AVAILABLE:
        sound_check = tk.Checkbutton(main_frame, text="Phat chuong keu khi nhac", variable=sound_enabled, bg=theme["bg"], fg=theme["text"], activebackground=theme["bg"], activeforeground=theme["text"], selectcolor=theme["bg"], font=("Times New Roman", 11))
        sound_check.pack(anchor="w", pady=4)

    button_frame = tk.Frame(main_frame, bg=theme["bg"])
    button_frame.pack(fill=tk.X, pady=8)

    reminders = load_reminders()
    reminders_active = False

    def refresh_list():
        reminder_list.delete(0, tk.END)
        for idx, item in enumerate(reminders, start=1):
            when = item["time"].strftime("%d/%m/%Y %H:%M")
            offset = item["offset"]
            status = "X" if item["sent"] else "o"
            title = item["title"]
            text = "%d. %s — %s (truoc %d phut) [%s]" % (idx, title, when, offset, status)
            reminder_list.insert(tk.END, text)
        save_reminders(reminders)

    def add_reminder():
        title = title_entry.get().strip()
        date_text = date_entry.get().strip()
        time_text = time_entry.get().strip()
        offset_text = offset_entry.get().strip()

        if not title:
            messagebox.showwarning("Loi", "Nhap tieu de nhac viec.")
            return
        try:
            remind_time = datetime.strptime(f"{date_text} {time_text}", "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showwarning("Loi", "Ngay hoac gio khong dung dinh dang.")
            return
        try:
            offset = int(offset_text)
            if offset < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Loi", "Nhac truoc phai la so khong am.")
            return
        if remind_time < datetime.now():
            messagebox.showwarning("Loi", "Thoi gian nhac phai la trong tuong lai.")
            return

        reminders.append({
            "title": title,
            "time": remind_time,
            "offset": offset,
            "sent": False,
        })
        refresh_list()
        title_entry.delete(0, tk.END)
        status_label.config(text="Da them nhac nho. (da luu)", fg="#27ae60")

    def remove_reminder():
        selection = reminder_list.curselection()
        if not selection:
            messagebox.showinfo("Thong bao", "Chon nhac viec de xoa.")
            return
        index = selection[0]
        del reminders[index]
        refresh_list()
        status_label.config(text="Da xoa nhac nho. (da luu)", fg="#27ae60")

    def check_reminders():
        nonlocal reminders_active
        now = datetime.now()
        for item in reminders:
            if not item["sent"]:
                remind_at = item["time"] - timedelta(minutes=item["offset"])
                if now >= remind_at:
                    item["sent"] = True
                    save_reminders(reminders)
                    refresh_list()
                    if sound_enabled.get() and SOUND_AVAILABLE:
                        try:
                            winsound.Beep(1000, 500)
                            import time
                            time.sleep(0.2)
                            winsound.Beep(1000, 500)
                            time.sleep(0.2)
                            winsound.Beep(1000, 500)
                        except Exception:
                            pass
                    title = item["title"]
                    when = item["time"].strftime("%H:%M %d/%m/%Y")
                    messagebox.showinfo("Nhac viec", "%s\nThoi gian: %s" % (title, when))
        if reminders_active:
            win.after(5000, check_reminders)

    def start_reminders():
        nonlocal reminders_active
        if not reminders:
            messagebox.showwarning("Loi", "Chua co nhac viec nao.")
            return
        reminders_active = True
        status_label.config(text="Nhac viec dang chay...", fg="#e74c3c")
        check_reminders()

    def stop_reminders():
        nonlocal reminders_active
        reminders_active = False
        status_label.config(text="Nhac viec da dung.", fg=theme["label_color"])

    tk.Button(button_frame, text="Them nhac", width=11, command=add_reminder, bg="#27ae60", fg="white", font=("Times New Roman", 11, "bold"), relief=tk.FLAT, padx=10, pady=6).pack(side=tk.LEFT, padx=4)
    tk.Button(button_frame, text="Xoa nhac", width=11, command=remove_reminder, bg="#e74c3c", fg="white", font=("Times New Roman", 11, "bold"), relief=tk.FLAT, padx=10, pady=6).pack(side=tk.LEFT, padx=4)
    tk.Button(button_frame, text="Bat dau", width=11, command=start_reminders, bg="#3498db", fg="white", font=("Times New Roman", 11, "bold"), relief=tk.FLAT, padx=10, pady=6).pack(side=tk.LEFT, padx=4)
    tk.Button(button_frame, text="Dung", width=11, command=stop_reminders, bg="#95a5a6", fg="white", font=("Times New Roman", 11, "bold"), relief=tk.FLAT, padx=10, pady=6).pack(side=tk.LEFT, padx=4)

    refresh_list()
    status_label.config(text="Da tai %d nhac viec tu file." % len(reminders), fg="#27ae60")

    # Tu dong bat dau kiem tra nhac viec neu co
    if reminders:
        reminders_active = True
        status_label.config(text="Nhac viec dang chay tu dong...", fg="#e74c3c")
        check_reminders()

    win.protocol("WM_DELETE_WINDOW", lambda: [stop_reminders(), win.destroy()])
