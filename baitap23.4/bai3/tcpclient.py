import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8090))

data = input("Nhập mật khẩu (cách nhau bằng dấu phẩy): ")

client.send(data.encode())

result = client.recv(1024).decode()

print("✅ Mật khẩu hợp lệ:", result)

client.close()