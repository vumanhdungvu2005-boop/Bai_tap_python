# Nhập số nguyên dương
n = int(input("Nhập số nguyên dương: "))

# Kiểm tra chia hết cho cả 2 và 3 (tức chia hết cho 6)
if n % 2 == 0 and n % 3 == 0:
    print("Số này chia hết cho cả 2 và 3")

# Chỉ chia hết cho 2
elif n % 2 == 0:
    print("Số này chỉ chia hết cho 2")

# Chỉ chia hết cho 3
elif n % 3 == 0:
    print("Số này chỉ chia hết cho 3")

# Không chia hết cho cả 2 và 3
else:
    print("Số này không chia hết cho 2 và 3")