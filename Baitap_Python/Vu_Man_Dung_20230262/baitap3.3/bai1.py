# Nhập một số nguyên từ bàn phím
n = int(input("Nhập số nguyên dương: "))

# Toán tử % là phép chia lấy dư
# Nếu n chia 2 dư 0 => số chẵn
if n % 2 == 0:
    print("Đây là một số chẵn")
else:
    # Ngược lại => số lẻ
    print("Đây là một số lẻ")