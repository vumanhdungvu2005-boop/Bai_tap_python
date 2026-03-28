# Nhập 3 số nguyên từ bàn phím
a = int(input("Nhập a: "))
b = int(input("Nhập b: "))
c = int(input("Nhập c: "))

# Điều kiện để 3 cạnh tạo thành tam giác:
# Tổng 2 cạnh bất kỳ phải lớn hơn cạnh còn lại
if a + b > c and a + c > b and b + c > a:
    print("Độ dài ba cạnh tam giác")
else:
    # Nếu không thỏa mãn điều kiện trên
    print("Đây không phải độ dài ba cạnh tam giác")