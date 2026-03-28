# Bài 3

# Nhập dữ liệu
a = int(input("Nhập số a: "))
b = int(input("Nhập số b: "))
c = int(input("Nhập số c: "))

# a) Tổng và tích
print("\nTổng =", a + b + c)
print("Tích =", a * b * c)

# b) Hiệu
print("\nHiệu:")
print("a - b =", a - b)
print("a - c =", a - c)
print("b - c =", b - c)

# c) Phép chia (lấy a và b)
print("\nPhép chia (a và b):")
if b != 0:
    print("a // b =", a // b)
    print("a % b =", a % b)
    print("a / b =", a / b)
else:
    print("Không thể chia cho 0")