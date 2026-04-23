import socket

HOST = '127.0.0.1'   # Localhost
PORT = 9090          # Port yêu cầu

# Tạo socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Gán địa chỉ và port
server.bind((HOST, PORT))

# Lắng nghe kết nối
server.listen(1)

print("🟢 Server đang chạy...")

while True:
    conn, addr = server.accept()
    print(f"🔗 Kết nối từ: {addr}")

    # Nhận dữ liệu từ client
    data = conn.recv(1024).decode()
    print("📩 Server nhận:", data)

    # Gửi phản hồi lại client
    message = "From SERVER TCP"
    conn.send(message.encode())

    conn.close()
    print("❌ Đóng kết nối\n")