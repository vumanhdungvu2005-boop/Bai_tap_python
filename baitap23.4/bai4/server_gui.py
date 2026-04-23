import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345

# GUI
window = tk.Tk()
window.title("Server Chat - Pink Edition")
window.geometry("640x620")
window.config(bg="#fff1f8")
window.resizable(True, True)

# Set theme
style = ttk.Style()
style.theme_use('clam')  # Modern theme

# Configure styles
style.configure("Accent.TButton", 
                font=("Segoe UI", 12, "bold"), 
                padding=10,
                relief="flat",
                background="#d946ef",
                foreground="#ffffff")
style.map("Accent.TButton",
          background=[('active', '#be185d')],
          foreground=[('active', '#ffffff'), ('disabled', '#f9a8d4')])

style.configure("Secondary.TButton",
                font=("Segoe UI", 10, "bold"),
                padding=7,
                relief="flat",
                background="#f9a8d4",
                foreground="#831843")

style.configure("TEntry", 
                font=("Segoe UI", 12),
                padding=5,
                relief="flat")

# Header frame
header_frame = tk.Frame(window, bg="#fde7f7", height=56)
header_frame.pack(fill=tk.X, padx=12, pady=(12,0))
header_frame.pack_propagate(False)

title_label = tk.Label(header_frame, 
                      text="✨ Server Chat", 
                      font=("Segoe UI", 18, "bold"), 
                      bg="#fde7f7", 
                      fg="#831843")
title_label.pack(side=tk.LEFT, padx=20)

sub_label = tk.Label(header_frame,
                     text="Chuyên nghiệp, nhẹ nhàng và tươi tắn",
                     font=("Segoe UI", 10),
                     bg="#fde7f7",
                     fg="#9d174d")
sub_label.pack(side=tk.RIGHT, padx=20)

# Status panel
status_frame = tk.Frame(window, bg="#fff1f8", pady=8)
status_frame.pack(fill=tk.X, padx=14, pady=(10, 0))

status_badge = tk.Label(status_frame,
                        text="⏳ Đang chờ kết nối...",
                        font=("Segoe UI", 10, "bold"),
                        bg="#f9a8d4",
                        fg="#831843",
                        padx=12,
                        pady=6)
status_badge.pack(side=tk.LEFT)

# Main card
main_frame = tk.Frame(window, bg="#fff1f8", bd=0)
main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

chat_card = tk.Frame(main_frame, bg="#fff7fd", bd=0, relief="ridge", highlightthickness=1, highlightbackground="#f9c2ed")
chat_card.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

chat_box = scrolledtext.ScrolledText(chat_card, 
                                   wrap=tk.WORD, 
                                   font=("Segoe UI", 11), 
                                   bg="#fff4fb", 
                                   fg="#581c87",
                                   relief="flat",
                                   padx=14,
                                   pady=14,
                                   insertbackground="#d946ef")
chat_box.pack(fill=tk.BOTH, expand=True)
chat_box.config(state='disabled')

# Input frame with visible send button
input_frame = tk.Frame(main_frame, bg="#fff1f8", pady=8)
input_frame.pack(fill=tk.X)

entry = tk.Entry(input_frame, 
                font=("Segoe UI", 12), 
                bg="#fff4fb", 
                fg="#581c87",
                relief="flat",
                insertbackground="#d946ef")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 10), pady=4, ipady=9)

send_button = ttk.Button(input_frame, 
                        text="📤 Gửi", 
                        style="Accent.TButton",
                        command=lambda: send())
send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=4)

def display(msg, sender="system"):
    chat_box.config(state='normal')
    if sender == "client":
        chat_box.insert(tk.END, f"👤 Client: {msg}\n", "client")
    elif sender == "server":
        chat_box.insert(tk.END, f"🖥️  Bạn: {msg}\n", "server")
    else:
        chat_box.insert(tk.END, f"ℹ️  {msg}\n", "system")
    chat_box.config(state='disabled')
    chat_box.yview(tk.END)

# Configure tags for different message types
chat_box.tag_configure("client", foreground="#e74c3c", font=("Segoe UI", 11, "bold"))
chat_box.tag_configure("server", foreground="#27ae60", font=("Segoe UI", 11, "bold"))
chat_box.tag_configure("system", foreground="#7f8c8d", font=("Segoe UI", 10, "italic"))

def update_status(text):
    status_badge.config(text=text)

# Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind((HOST, PORT))
    server.listen(1)
    conn = None  # Initialize conn
    display("Khởi động server thành công!")
except OSError as e:
    messagebox.showerror("Lỗi socket", f"Không thể sử dụng cổng {PORT}: {e}")
    window.destroy()
    raise

def start_server():
    global conn, addr
    try:
        conn, addr = server.accept()
        display(f"Kết nối thành công từ {addr}", "system")
        update_status(f"🟢 Đã kết nối: {addr}")
        threading.Thread(target=receive, daemon=True).start()
    except Exception as e:
        display(f"Lỗi kết nối: {e}", "system")

def receive():
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                display(msg, "client")
        except:
            display("Mất kết nối với client", "system")
            update_status("🔴 Mất kết nối")
            break

def send(event=None):
    if conn is None:
        messagebox.showwarning("Cảnh báo", "Chưa có client kết nối!")
        return
    msg = entry.get().strip()
    if msg:
        try:
            conn.send(msg.encode())
            display(msg, "server")
            entry.delete(0, tk.END)
        except:
            display("Lỗi gửi tin nhắn", "system")
            update_status("🔴 Lỗi kết nối")

entry.bind("<Return>", send)

threading.Thread(target=start_server, daemon=True).start()

window.mainloop()