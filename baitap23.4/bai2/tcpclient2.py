import socket

HOST = '127.0.0.1'
PORT = 8090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Nhập 2 số
a = input("Nhập số a: ")
b = input("Nhập số b: ")

message = f"{a} {b}"
client.send(message.encode())

data = client.recv(1024).decode()
print("📩 Kết quả từ server:", data)

client.close()