import math

# Hình tròn
def chu_vi_hinh_tron(r):
    return 2 * math.pi * r

def dien_tich_hinh_tron(r):
    return math.pi * r * r

# Hình chữ nhật
def chu_vi_hcn(dai, rong):
    return 2 * (dai + rong)

def dien_tich_hcn(dai, rong):
    return dai * rong