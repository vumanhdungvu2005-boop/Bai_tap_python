import socket

HOST = '127.0.0.1'
PORT = 9090

# Tạo socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối tới server
client.connect((HOST, PORT))

# Gửi dữ liệu lên server
message = "From CLIENT TCP"
client.send(message.encode())

# Nhận phản hồi từ server
data = client.recv(1024).decode()
print("📩 Client nhận:", data)

client.close()