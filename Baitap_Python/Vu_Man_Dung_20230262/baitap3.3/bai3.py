# Import thư viện time để lấy thời gian hiện tại
import time

# Nhập năm sinh
nam_sinh = int(input("Nhập năm sinh: "))

# Lấy thời gian hiện tại của hệ thống
x = time.localtime()

# x là một tuple (dạng danh sách)
# x[0] chính là năm hiện tại
nam_hien_tai = x[0]

# Tính tuổi = năm hiện tại - năm sinh
tuoi = nam_hien_tai - nam_sinh

# In kết quả ra màn hình
print(f"Năm sinh {nam_sinh}, vậy bạn {tuoi} tuổi")