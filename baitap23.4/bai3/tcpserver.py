import socket
import re

def check_password(pw):
    if (6 <= len(pw) <= 12 and
        re.search("[a-z]", pw) and
        re.search("[A-Z]", pw) and
        re.search("[0-9]", pw) and
        re.search("[$#@]", pw)):
        return True
    return False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8090))
server.listen(1)

print("🟢 Server đang chạy...")

conn, addr = server.accept()
print("📡 Kết nối từ:", addr)

data = conn.recv(1024).decode()
print("📩 Nhận từ client:", data)

passwords = data.split(",")

valid_pw = [pw for pw in passwords if check_password(pw)]

result = ",".join(valid_pw)

conn.send(result.encode())

conn.close()
server.close()