import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ast

# ================== FILE ==================
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ================== LOAD KEY ==================
def load_key(path):
    try:
        content = read_file(path)
        key_dict = ast.literal_eval(content)

        if not isinstance(key_dict, dict):
            raise ValueError("File key không hợp lệ!")

        new_dict = {}
        for k, v in key_dict.items():
            new_dict[k] = v
            new_dict[k.upper()] = v

        return new_dict

    except Exception as e:
        messagebox.showerror("Lỗi key", str(e))
        return None


# ================== ENCODE / DECODE ==================
def encode(text, key_dict):
    result = ""
    count = 0
    positions = []

    for i, ch in enumerate(text):
        if ch in key_dict:
            result += key_dict[ch]
            count += 1
            positions.append(i)
        else:
            result += ch

    return result, count, positions


def decode(text, key_dict):
    decode_dict = {v: k for k, v in key_dict.items()}
    result = ""

    for ch in text:
        result += decode_dict.get(ch, ch)

    return result


# ================== GUI ==================
def choose_key():
    path = filedialog.askopenfilename(title="Chọn file key")
    entry_key.delete(0, tk.END)
    entry_key.insert(0, path)

def choose_input():
    path = filedialog.askopenfilename(title="Chọn file input")
    entry_input.delete(0, tk.END)
    entry_input.insert(0, path)

    if path:
        text = read_file(path)
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, text)


def highlight(positions):
    output_text.tag_remove("highlight", "1.0", tk.END)

    for pos in positions:
        idx = f"1.0+{pos}c"
        output_text.tag_add("highlight", idx, f"{idx}+1c")

    output_text.tag_config("highlight", foreground="red")


def process(mode):
    key_path = entry_key.get()
    input_path = entry_input.get()

    if not key_path or not input_path:
        messagebox.showerror("Lỗi", "Chọn đủ file!")
        return

    key_dict = load_key(key_path)
    if not key_dict:
        return

    text = input_text.get("1.0", tk.END)

    if mode == "encode":
        result, count, pos = encode(text, key_dict)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        highlight(pos)

        lbl_status.config(text=f"✔ Đã mã hóa {count} ký tự")

    else:
        result = decode(text, key_dict)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

        lbl_status.config(text="✔ Đã giải mã")


def save_file():
    content = output_text.get("1.0", tk.END)
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        write_file(path, content)
        messagebox.showinfo("OK", "Đã lưu file!")


def copy_output():
    content = output_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    messagebox.showinfo("Copy", "Đã copy!")


# ================== WINDOW ==================
root = tk.Tk()
root.title("Encryption Tool Pro")
root.geometry("900x600")

# STYLE
style = ttk.Style()
style.theme_use("clam")

# ===== TOP FRAME =====
frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill="x")

ttk.Label(frame_top, text="File KEY:").grid(row=0, column=0, sticky="w")
entry_key = ttk.Entry(frame_top, width=60)
entry_key.grid(row=0, column=1)
ttk.Button(frame_top, text="Browse", command=choose_key).grid(row=0, column=2)

ttk.Label(frame_top, text="File INPUT:").grid(row=1, column=0, sticky="w")
entry_input = ttk.Entry(frame_top, width=60)
entry_input.grid(row=1, column=1)
ttk.Button(frame_top, text="Browse", command=choose_input).grid(row=1, column=2)

# ===== BUTTONS =====
frame_btn = ttk.Frame(root, padding=10)
frame_btn.pack()

ttk.Button(frame_btn, text="Mã hóa", command=lambda: process("encode")).grid(row=0, column=0, padx=5)
ttk.Button(frame_btn, text="Giải mã", command=lambda: process("decode")).grid(row=0, column=1, padx=5)
ttk.Button(frame_btn, text="Lưu file", command=save_file).grid(row=0, column=2, padx=5)
ttk.Button(frame_btn, text="Copy", command=copy_output).grid(row=0, column=3, padx=5)

# ===== TEXT AREA =====
frame_text = ttk.Frame(root)
frame_text.pack(fill="both", expand=True)

# INPUT
frame_in = ttk.Frame(frame_text)
frame_in.pack(side="left", fill="both", expand=True, padx=5)

ttk.Label(frame_in, text="INPUT").pack()
scroll_in = ttk.Scrollbar(frame_in)
scroll_in.pack(side="right", fill="y")

input_text = tk.Text(frame_in, yscrollcommand=scroll_in.set)
input_text.pack(fill="both", expand=True)
scroll_in.config(command=input_text.yview)

# OUTPUT
frame_out = ttk.Frame(frame_text)
frame_out.pack(side="right", fill="both", expand=True, padx=5)

ttk.Label(frame_out, text="OUTPUT").pack()
scroll_out = ttk.Scrollbar(frame_out)
scroll_out.pack(side="right", fill="y")

output_text = tk.Text(frame_out, yscrollcommand=scroll_out.set)
output_text.pack(fill="both", expand=True)
scroll_out.config(command=output_text.yview)

# STATUS
lbl_status = ttk.Label(root, text="Sẵn sàng", relief="sunken", anchor="w")
lbl_status.pack(fill="x", side="bottom")

root.mainloop()