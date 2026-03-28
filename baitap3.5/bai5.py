import math  # Thư viện dùng để tính căn bậc 2 (sqrt)

# Nhập 3 hệ số a, b, c
a = float(input("Nhập a: "))
b = float(input("Nhập b: "))
c = float(input("Nhập c: "))

# Trường hợp a = 0 => không phải phương trình bậc 2
if a == 0:
    print("Đây không phải phương trình bậc 2")

    # Khi đó trở thành phương trình bậc 1: bx + c = 0
    if b == 0:
        if c == 0:
            print("Phương trình vô số nghiệm")
        else:
            print("Phương trình vô nghiệm")
    else:
        x = -c / b
        print("Nghiệm x =", x)

else:
    # Tính delta (Δ = b² - 4ac)
    delta = b**2 - 4*a*c

    # Nếu delta < 0 => vô nghiệm
    if delta < 0:
        print("Phương trình vô nghiệm")

    # Nếu delta = 0 => nghiệm kép
    elif delta == 0:
        x = -b / (2*a)
        print("Phương trình có nghiệm kép x =", x)

    # Nếu delta > 0 => 2 nghiệm phân biệt
    else:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print("Phương trình có 2 nghiệm:")
        print("x1 =", x1)
        print("x2 =", x2)