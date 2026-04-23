import socket

HOST = '127.0.0.1'
PORT = 8090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print("🟢 Server đang chạy...")

while True:
    conn, addr = server.accept()
    print(f"🔗 Kết nối từ: {addr}")

    data = conn.recv(1024).decode()
    print("📩 Nhận:", data)

    try:
        # Tách 2 số
        a, b = map(float, data.split())
        result = a + b
        message = f"Tổng = {result}"
    except:
        message = "❌ Dữ liệu không hợp lệ"

    conn.send(message.encode())
    conn.close()