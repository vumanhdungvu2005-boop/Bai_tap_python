import math

class PhanSo:
    def __init__(self, tu=0, mau=1):
        if mau == 0:
            raise ValueError("Mẫu số không được bằng 0!")
        self.tu = tu
        self.mau = mau
        self.rut_gon()

    # Rút gọn phân số
    def rut_gon(self):
        ucln = math.gcd(self.tu, self.mau)
        self.tu //= ucln
        self.mau //= ucln

        # Đưa dấu âm lên tử
        if self.mau < 0:
            self.tu *= -1
            self.mau *= -1

    # Cộng
    def cong(self, other):
        tu = self.tu * other.mau + self.mau * other.tu
        mau = self.mau * other.mau
        return PhanSo(tu, mau)

    # Trừ
    def tru(self, other):
        tu = self.tu * other.mau - self.mau * other.tu
        mau = self.mau * other.mau
        return PhanSo(tu, mau)

    # Nhân
    def nhan(self, other):
        return PhanSo(self.tu * other.tu, self.mau * other.mau)

    # Chia
    def chia(self, other):
        if other.tu == 0:
            raise ValueError("Không thể chia cho 0!")
        return PhanSo(self.tu * other.mau, self.mau * other.tu)

    # Hiển thị
    def __str__(self):
        return f"{self.tu}/{self.mau}"
    # ====== TEST ======
if __name__ == "__main__":
    a = PhanSo(1, 2)
    b = PhanSo(3, 4)

    print("a =", a)
    print("b =", b)

    print("Cộng:", a.cong(b))
    print("Trừ:", a.tru(b))
    print("Nhân:", a.nhan(b))
    print("Chia:", a.chia(b))