import sys
import pyodbc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# ====== CẤU HÌNH ======
SERVER = "MANH-DUNG-VU\\SQLEXPRESS03"
DATABASE = "QuanLyBanHang"

# Stylesheet chung - hiện đại & đẹp
STYLESHEET = """
QMainWindow {
    background-color: #f0f2f5;
}

/* Buttons - Modern Blue Style */
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 600;
    font-size: 11px;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QPushButton:hover {
    background-color: #1d4ed8;
    border: 1px solid #1e40af;
}
QPushButton:pressed {
    background-color: #1e3a8a;
    padding: 9px 13px;
}

/* Input Fields - Clean Style */
QLineEdit {
    border: 2px solid #e5e7eb;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 11px;
    font-family: 'Segoe UI', Arial, sans-serif;
    background-color: #ffffff;
}
QLineEdit:focus {
    border: 2px solid #2563eb;
    background-color: #f9fafb;
}
QLineEdit:hover {
    border: 2px solid #d1d5db;
}

/* Labels - Professional */
QLabel {
    font-size: 11px;
    color: #1f2937;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-weight: 500;
}

/* Tables - Modern Design */
QTableWidget {
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    gridline-color: #f3f4f6;
    background-color: #ffffff;
    alternate-background-color: #f9fafb;
}
QTableWidget::item {
    padding: 6px;
    border-bottom: 1px solid #f3f4f6;
}
QTableWidget::item:selected {
    background-color: #dbeafe;
    color: #000;
}
QHeaderView::section {
    background-color: #f3f4f6;
    color: #1f2937;
    padding: 8px;
    border: none;
    border-right: 1px solid #e5e7eb;
    font-weight: 600;
    font-size: 11px;
}

/* GroupBox - Modern */
QGroupBox {
    border: 2px solid #e5e7eb;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 600;
    color: #1f2937;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px 0 4px;
    color: #2563eb;
}

/* Tabs - Modern Style */
QTabWidget::pane {
    border: 1px solid #e5e7eb;
    border-radius: 6px;
}
QTabBar::tab {
    background-color: #f3f4f6;
    color: #6b7280;
    padding: 10px 24px;
    border: none;
    font-weight: 600;
    font-size: 11px;
    border-radius: 6px 6px 0 0;
    margin-right: 2px;
}
QTabBar::tab:hover {
    background-color: #e5e7eb;
}
QTabBar::tab:selected {
    background-color: #2563eb;
    color: white;
    border-bottom: 3px solid #1e40af;
}

/* MessageBox & Dialogs */
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #1f2937;
}
QMessageBox QDialogButtonBox QPushButton {
    min-width: 80px;
}
"""

# ====== CẤU HÌNH ======
SERVER = "MANH-DUNG-VU\\SQLEXPRESS03"
DATABASE = "QuanLyBanHang"

def connect():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

# ====== MAIN WINDOW ======
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏪 Quản Lý Bán Hàng - Sales Management System")
        self.resize(1300, 750)
        self.setStyleSheet(STYLESHEET)
        
        # Set window icon background
        self.setWindowOpacity(1.0)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_mat_hang()
        self.init_khach_hang()
        self.init_don_hang()

        # Timer để tự động refresh dữ liệu mỗi 10 giây
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(10000)  # 10 giây

    def refresh_all(self):
        self.load_mat_hang()
        self.load_khach_hang()
        self.load_don_hang()

    # ================= MẶT HÀNG =================
    def init_mat_hang(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("📦 QUẢN LÝ MẶT HÀNG")
        title_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2563eb; margin-bottom: 5px;")

        # Nhóm form nhập liệu
        form_group = QGroupBox("Thông tin mặt hàng")
        form_layout = QGridLayout()
        form_layout.setSpacing(10)
        
        self.mh_ma = QLineEdit(); self.mh_ma.setPlaceholderText("Nhập mã mặt hàng")
        self.mh_ten = QLineEdit(); self.mh_ten.setPlaceholderText("Nhập tên mặt hàng")
        self.mh_nguon = QLineEdit(); self.mh_nguon.setPlaceholderText("Nhập nguồn gốc")
        self.mh_gia = QLineEdit(); self.mh_gia.setPlaceholderText("Nhập giá bán")

        form_layout.addWidget(QLabel("Mã mặt hàng:"), 0, 0)
        form_layout.addWidget(self.mh_ma, 0, 1)
        form_layout.addWidget(QLabel("Tên mặt hàng:"), 0, 2)
        form_layout.addWidget(self.mh_ten, 0, 3)
        
        form_layout.addWidget(QLabel("Nguồn gốc:"), 1, 0)
        form_layout.addWidget(self.mh_nguon, 1, 1)
        form_layout.addWidget(QLabel("Giá bán:"), 1, 2)
        form_layout.addWidget(self.mh_gia, 1, 3)
        
        form_group.setLayout(form_layout)
        
        # Nhóm nút chức năng
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_add = QPushButton("➕ Thêm mới")
        btn_update = QPushButton("✏️ Cập nhật")
        btn_delete = QPushButton("🗑️ Xóa")
        btn_add.clicked.connect(self.them_mat_hang)
        btn_update.clicked.connect(self.sua_mat_hang)
        btn_delete.clicked.connect(self.xoa_mat_hang)
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        
        # Nhóm tìm kiếm
        search_group = QGroupBox("Tìm kiếm mặt hàng")
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        self.mh_search = QLineEdit(); self.mh_search.setPlaceholderText("🔍 Tìm theo mã / tên / nguồn gốc...")
        btn_search = QPushButton("🔍 Tìm")
        btn_clear = QPushButton("❌ Xóa tìm")
        btn_search.clicked.connect(self.tim_mat_hang)
        btn_clear.clicked.connect(self.load_mat_hang)
        
        search_layout.addWidget(self.mh_search)
        search_layout.addWidget(btn_search, 0)
        search_layout.addWidget(btn_clear, 0)
        search_group.setLayout(search_layout)

        self.mh_table = QTableWidget()
        self.mh_table.setColumnCount(4)
        self.mh_table.setHorizontalHeaderLabels(["Mã", "Tên mặt hàng", "Nguồn gốc", "Giá"])
        self.mh_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.mh_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.mh_table.setAlternatingRowColors(True)
        self.mh_table.horizontalHeader().setStretchLastSection(True)
        self.mh_table.setRowHeight(0, 30)
        self.mh_table.itemSelectionChanged.connect(self.select_mat_hang)

        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addLayout(btn_layout)
        layout.addWidget(search_group)
        layout.addWidget(QLabel("📋 Danh sách mặt hàng:"))
        layout.addWidget(self.mh_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "📦 Mặt hàng")

        self.load_mat_hang()

    def load_mat_hang(self, keyword=None):
        try:
            conn = connect()
            cursor = conn.cursor()
            if keyword:
                pattern = f"%{keyword}%"
                cursor.execute(
                    "SELECT * FROM MatHang WHERE MaHang LIKE ? OR TenHang LIKE ? OR NguonGoc LIKE ?",
                    (pattern, pattern, pattern)
                )
            else:
                cursor.execute("SELECT * FROM MatHang")

            self.mh_table.setRowCount(0)
            for row_data in cursor:
                row = self.mh_table.rowCount()
                self.mh_table.insertRow(row)
                for col, data in enumerate(row_data):
                    self.mh_table.setItem(row, col, QTableWidgetItem(str(data)))

            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def them_mat_hang(self):
        try:
            ma = self.mh_ma.text().strip()
            ten = self.mh_ten.text().strip()
            nguon = self.mh_nguon.text().strip()
            gia_text = self.mh_gia.text().strip()
            if not ma or not ten or not nguon or not gia_text:
                raise ValueError("Vui lòng nhập đầy đủ thông tin mặt hàng.")
            
            try:
                gia = float(gia_text)
            except ValueError:
                raise ValueError("Giá phải là số!")

            conn = connect()
            cursor = conn.cursor()
            
            # Kiểm tra mã hàng đã tồn tại không
            cursor.execute("SELECT COUNT(*) FROM MatHang WHERE MaHang = ?", (ma,))
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"Mã mặt hàng '{ma}' đã tồn tại! Vui lòng nhập mã khác.")
            
            cursor.execute(
                "INSERT INTO MatHang (MaHang, TenHang, NguonGoc, Gia) VALUES (?, ?, ?, ?)",
                (ma, ten, nguon, gia)
            )
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Thành công", f"Thêm mặt hàng '{ten}' thành công!")
            self.mh_ma.clear()
            self.mh_ten.clear()
            self.mh_nguon.clear()
            self.mh_gia.clear()
            self.load_mat_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def sua_mat_hang(self):
        try:
            ma = self.mh_ma.text().strip()
            ten = self.mh_ten.text().strip()
            nguon = self.mh_nguon.text().strip()
            gia_text = self.mh_gia.text().strip()
            if not ma:
                raise ValueError("Chọn hoặc nhập mã mặt hàng để sửa.")
            if not ten or not nguon or not gia_text:
                raise ValueError("Vui lòng nhập đầy đủ thông tin mặt hàng.")
            gia = float(gia_text)

            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE MatHang SET TenHang = ?, NguonGoc = ?, Gia = ? WHERE MaHang = ?",
                (ten, nguon, gia, ma)
            )
            conn.commit()
            conn.close()
            self.load_mat_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def xoa_mat_hang(self):
        try:
            ma = self.mh_ma.text().strip()
            if not ma:
                raise ValueError("Chọn mặt hàng để xóa.")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MatHang WHERE MaHang = ?", (ma,))
            conn.commit()
            conn.close()
            self.mh_ma.clear()
            self.mh_ten.clear()
            self.mh_nguon.clear()
            self.mh_gia.clear()
            self.load_mat_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def select_mat_hang(self):
        items = self.mh_table.selectedItems()
        if not items:
            return
        self.mh_ma.setText(items[0].text())
        self.mh_ten.setText(items[1].text())
        self.mh_nguon.setText(items[2].text())
        self.mh_gia.setText(items[3].text())

    def tim_mat_hang(self):
        self.load_mat_hang(self.mh_search.text().strip())

    # ================= KHÁCH HÀNG =================
    def init_khach_hang(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("👥 QUẢN LÝ KHÁCH HÀNG")
        title_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2563eb; margin-bottom: 5px;")

        # Nhóm form nhập liệu
        form_group = QGroupBox("Thông tin khách hàng")
        form_layout = QGridLayout()
        form_layout.setSpacing(10)
        
        self.kh_ma = QLineEdit(); self.kh_ma.setPlaceholderText("Nhập mã khách hàng")
        self.kh_ten = QLineEdit(); self.kh_ten.setPlaceholderText("Nhập tên khách hàng")
        self.kh_dc = QLineEdit(); self.kh_dc.setPlaceholderText("Nhập địa chỉ")
        self.kh_sdt = QLineEdit(); self.kh_sdt.setPlaceholderText("Nhập số điện thoại")

        form_layout.addWidget(QLabel("Mã khách hàng:"), 0, 0)
        form_layout.addWidget(self.kh_ma, 0, 1)
        form_layout.addWidget(QLabel("Tên khách hàng:"), 0, 2)
        form_layout.addWidget(self.kh_ten, 0, 3)
        
        form_layout.addWidget(QLabel("Địa chỉ:"), 1, 0)
        form_layout.addWidget(self.kh_dc, 1, 1)
        form_layout.addWidget(QLabel("Số điện thoại:"), 1, 2)
        form_layout.addWidget(self.kh_sdt, 1, 3)
        
        form_group.setLayout(form_layout)
        
        # Nhóm nút chức năng
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_add = QPushButton("➕ Thêm mới")
        btn_update = QPushButton("✏️ Cập nhật")
        btn_delete = QPushButton("🗑️ Xóa")
        btn_add.clicked.connect(self.them_khach_hang)
        btn_update.clicked.connect(self.sua_khach_hang)
        btn_delete.clicked.connect(self.xoa_khach_hang)
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        
        # Nhóm tìm kiếm
        search_group = QGroupBox("Tìm kiếm khách hàng")
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        self.kh_search = QLineEdit(); self.kh_search.setPlaceholderText("🔍 Tìm theo mã / tên / địa chỉ...")
        btn_search = QPushButton("🔍 Tìm")
        btn_clear = QPushButton("❌ Xóa tìm")
        btn_search.clicked.connect(self.tim_khach_hang)
        btn_clear.clicked.connect(self.load_khach_hang)
        
        search_layout.addWidget(self.kh_search)
        search_layout.addWidget(btn_search, 0)
        search_layout.addWidget(btn_clear, 0)
        search_group.setLayout(search_layout)

        self.kh_table = QTableWidget()
        self.kh_table.setColumnCount(4)
        self.kh_table.setHorizontalHeaderLabels(["Mã KH", "Tên khách hàng", "Địa chỉ", "Điện thoại"])
        self.kh_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.kh_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.kh_table.setAlternatingRowColors(True)
        self.kh_table.horizontalHeader().setStretchLastSection(True)
        self.kh_table.setRowHeight(0, 30)
        self.kh_table.itemSelectionChanged.connect(self.select_khach_hang)

        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addLayout(btn_layout)
        layout.addWidget(search_group)
        layout.addWidget(QLabel("📋 Danh sách khách hàng:"))
        layout.addWidget(self.kh_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "👥 Khách hàng")

        self.load_khach_hang()

    def load_khach_hang(self, keyword=None):
        try:
            conn = connect()
            cursor = conn.cursor()
            if keyword:
                pattern = f"%{keyword}%"
                cursor.execute(
                    "SELECT * FROM KhachHang WHERE MaKH LIKE ? OR TenKH LIKE ? OR DiaChi LIKE ? OR SDT LIKE ?",
                    (pattern, pattern, pattern, pattern)
                )
            else:
                cursor.execute("SELECT * FROM KhachHang")

            self.kh_table.setRowCount(0)
            for row_data in cursor:
                row = self.kh_table.rowCount()
                self.kh_table.insertRow(row)
                for col, data in enumerate(row_data):
                    self.kh_table.setItem(row, col, QTableWidgetItem(str(data)))

            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def them_khach_hang(self):
        try:
            ma = self.kh_ma.text().strip()
            ten = self.kh_ten.text().strip()
            dc = self.kh_dc.text().strip()
            sdt = self.kh_sdt.text().strip()
            if not ma or not ten or not dc or not sdt:
                raise ValueError("Vui lòng nhập đầy đủ thông tin khách hàng.")

            conn = connect()
            cursor = conn.cursor()
            
            # Kiểm tra mã khách hàng đã tồn tại không
            cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE MaKH = ?", (ma,))
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"Mã khách hàng '{ma}' đã tồn tại! Vui lòng nhập mã khác.")
            
            cursor.execute(
                "INSERT INTO KhachHang (MaKH, TenKH, DiaChi, SDT) VALUES (?, ?, ?, ?)",
                (ma, ten, dc, sdt)
            )
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Thành công", f"Thêm khách hàng '{ten}' thành công!")
            self.kh_ma.clear()
            self.kh_ten.clear()
            self.kh_dc.clear()
            self.kh_sdt.clear()
            self.load_khach_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def sua_khach_hang(self):
        try:
            ma = self.kh_ma.text().strip()
            ten = self.kh_ten.text().strip()
            dc = self.kh_dc.text().strip()
            sdt = self.kh_sdt.text().strip()
            if not ma:
                raise ValueError("Chọn hoặc nhập mã khách hàng để sửa.")
            if not ten or not dc or not sdt:
                raise ValueError("Vui lòng nhập đầy đủ thông tin khách hàng.")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE KhachHang SET TenKH = ?, DiaChi = ?, SDT = ? WHERE MaKH = ?",
                (ten, dc, sdt, ma)
            )
            conn.commit()
            conn.close()
            self.load_khach_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def xoa_khach_hang(self):
        try:
            ma = self.kh_ma.text().strip()
            if not ma:
                raise ValueError("Chọn khách hàng để xóa.")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM KhachHang WHERE MaKH = ?", (ma,))
            conn.commit()
            conn.close()
            self.kh_ma.clear()
            self.kh_ten.clear()
            self.kh_dc.clear()
            self.kh_sdt.clear()
            self.load_khach_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def select_khach_hang(self):
        items = self.kh_table.selectedItems()
        if not items:
            return
        self.kh_ma.setText(items[0].text())
        self.kh_ten.setText(items[1].text())
        self.kh_dc.setText(items[2].text())
        self.kh_sdt.setText(items[3].text())

    def tim_khach_hang(self):
        self.load_khach_hang(self.kh_search.text().strip())

    # ================= ĐƠN HÀNG =================
    def init_don_hang(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("📋 QUẢN LÝ ĐƠN HÀNG")
        title_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2563eb; margin-bottom: 5px;")

        # Nhóm form nhập đơn hàng
        order_group = QGroupBox("Thông tin đơn hàng")
        order_layout = QGridLayout()
        order_layout.setSpacing(10)
        
        self.dh_ma = QLineEdit(); self.dh_ma.setPlaceholderText("Nhập mã đơn hàng")
        self.dh_makh = QLineEdit(); self.dh_makh.setPlaceholderText("Nhập mã khách hàng")
        
        order_layout.addWidget(QLabel("Mã đơn hàng:"), 0, 0)
        order_layout.addWidget(self.dh_ma, 0, 1)
        order_layout.addWidget(QLabel("Mã khách hàng:"), 0, 2)
        order_layout.addWidget(self.dh_makh, 0, 3)
        
        order_group.setLayout(order_layout)
        
        # Nhóm nút chức năng đơn hàng
        order_btn_layout = QHBoxLayout()
        order_btn_layout.setSpacing(10)
        
        btn_add = QPushButton("➕ Thêm mới")
        btn_update = QPushButton("✏️ Cập nhật")
        btn_delete = QPushButton("🗑️ Xóa")
        btn_add.clicked.connect(self.them_don_hang)
        btn_update.clicked.connect(self.sua_don_hang)
        btn_delete.clicked.connect(self.xoa_don_hang)
        
        order_btn_layout.addWidget(btn_add)
        order_btn_layout.addWidget(btn_update)
        order_btn_layout.addWidget(btn_delete)
        order_btn_layout.addStretch()
        
        # Nhóm tìm kiếm đơn hàng
        search_group = QGroupBox("Tìm kiếm đơn hàng")
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        self.dh_search = QLineEdit(); self.dh_search.setPlaceholderText("🔍 Tìm mã đơn / mã khách hàng...")
        btn_search = QPushButton("🔍 Tìm")
        btn_clear = QPushButton("❌ Xóa tìm")
        btn_search.clicked.connect(self.tim_don_hang)
        btn_clear.clicked.connect(self.load_don_hang)
        
        search_layout.addWidget(self.dh_search)
        search_layout.addWidget(btn_search, 0)
        search_layout.addWidget(btn_clear, 0)
        search_group.setLayout(search_layout)

        self.dh_table = QTableWidget()
        self.dh_table.setColumnCount(4)
        self.dh_table.setHorizontalHeaderLabels(["Mã đơn", "Mã KH", "Ngày đặt", "Tổng tiền"])
        self.dh_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.dh_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.dh_table.setAlternatingRowColors(True)
        self.dh_table.horizontalHeader().setStretchLastSection(True)
        self.dh_table.setRowHeight(0, 30)
        self.dh_table.cellClicked.connect(self.click_don)
        self.dh_table.itemSelectionChanged.connect(self.select_don_hang)

        # Nhóm chi tiết đơn hàng
        detail_group = QGroupBox("Chi tiết đơn hàng")
        detail_layout = QVBoxLayout()
        detail_layout.setSpacing(8)
        
        detail_form = QGridLayout()
        detail_form.setSpacing(8)
        
        self.ct_mahang = QLineEdit(); self.ct_mahang.setPlaceholderText("Nhập mã hàng")
        self.ct_soluong = QLineEdit(); self.ct_soluong.setPlaceholderText("Nhập số lượng")
        self.ct_dongia = QLineEdit(); self.ct_dongia.setPlaceholderText("Nhập đơn giá")
        
        detail_form.addWidget(QLabel("Mã hàng:"), 0, 0)
        detail_form.addWidget(self.ct_mahang, 0, 1)
        detail_form.addWidget(QLabel("Số lượng:"), 0, 2)
        detail_form.addWidget(self.ct_soluong, 0, 3)
        detail_form.addWidget(QLabel("Đơn giá:"), 0, 4)
        detail_form.addWidget(self.ct_dongia, 0, 5)
        
        detail_layout.addLayout(detail_form)
        
        detail_btn_layout = QHBoxLayout()
        detail_btn_layout.setSpacing(10)
        
        btn_add_ct = QPushButton("➕ Thêm mặt hàng")
        btn_del_ct = QPushButton("🗑️ Xóa mặt hàng")
        btn_refresh = QPushButton("🔄 Làm mới")
        btn_add_ct.clicked.connect(self.them_chi_tiet)
        btn_del_ct.clicked.connect(self.xoa_chi_tiet)
        btn_refresh.clicked.connect(lambda: [self.load_don_hang(), self.load_mat_hang(), self.load_khach_hang()])
        
        detail_btn_layout.addWidget(btn_add_ct)
        detail_btn_layout.addWidget(btn_del_ct)
        detail_btn_layout.addWidget(btn_refresh)
        detail_btn_layout.addStretch()
        
        detail_layout.addLayout(detail_btn_layout)
        
        self.ct_table = QTableWidget()
        self.ct_table.setColumnCount(5)
        self.ct_table.setHorizontalHeaderLabels(["Mã hàng", "Tên hàng", "SL", "Đơn giá", "Thành tiền"])
        self.ct_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ct_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ct_table.setAlternatingRowColors(True)
        self.ct_table.horizontalHeader().setStretchLastSection(True)
        self.ct_table.setRowHeight(0, 30)
        
        detail_layout.addWidget(QLabel("📦 Danh sách mặt hàng trong đơn:"))
        detail_layout.addWidget(self.ct_table)
        detail_group.setLayout(detail_layout)

        layout.addWidget(title)
        layout.addWidget(order_group)
        layout.addLayout(order_btn_layout)
        layout.addWidget(search_group)
        layout.addWidget(QLabel("📋 Danh sách đơn hàng:"))
        layout.addWidget(self.dh_table)
        layout.addWidget(detail_group)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "📦 Đơn hàng")

        self.load_don_hang()

    def load_don_hang(self, keyword=None):
        try:
            conn = connect()
            cursor = conn.cursor()
            if keyword:
                pattern = f"%{keyword}%"
                cursor.execute("""
                    SELECT d.MaDon, d.MaKH, d.Ngay,
                    ISNULL(SUM(ct.SoLuong * ct.DonGia), 0)
                    FROM DonHang d
                    LEFT JOIN ChiTietDonHang ct ON d.MaDon = ct.MaDon
                    WHERE d.MaDon LIKE ? OR d.MaKH LIKE ?
                    GROUP BY d.MaDon, d.MaKH, d.Ngay
                """, (pattern, pattern))
            else:
                cursor.execute("""
                    SELECT d.MaDon, d.MaKH, d.Ngay,
                    ISNULL(SUM(ct.SoLuong * ct.DonGia), 0)
                    FROM DonHang d
                    LEFT JOIN ChiTietDonHang ct ON d.MaDon = ct.MaDon
                    GROUP BY d.MaDon, d.MaKH, d.Ngay
                """)

            self.dh_table.setRowCount(0)
            for row_data in cursor:
                row = self.dh_table.rowCount()
                self.dh_table.insertRow(row)
                for col, data in enumerate(row_data):
                    self.dh_table.setItem(row, col, QTableWidgetItem(str(data)))

            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def order_exists(self, ma_don):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM DonHang WHERE MaDon = ?", (ma_don,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def customer_exists(self, ma_kh):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE MaKH = ?", (ma_kh,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def product_exists(self, ma_hang):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM MatHang WHERE MaHang = ?", (ma_hang,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def detail_exists(self, ma_don, ma_hang):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM ChiTietDonHang WHERE MaDon = ? AND MaHang = ?",
            (ma_don, ma_hang)
        )
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def clear_don_form(self):
        self.dh_ma.clear()
        self.dh_makh.clear()

    def clear_chi_tiet_form(self):
        self.ct_mahang.clear()
        self.ct_soluong.clear()
        self.ct_dongia.clear()

    def load_order_details(self, ma_don):
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.MaHang, m.TenHang, c.SoLuong, c.DonGia,
                c.SoLuong * c.DonGia
                FROM ChiTietDonHang c
                JOIN MatHang m ON c.MaHang = m.MaHang
                WHERE c.MaDon = ?
            """, (ma_don,))

            self.ct_table.setRowCount(0)
            for row_data in cursor:
                r = self.ct_table.rowCount()
                self.ct_table.insertRow(r)
                for c, data in enumerate(row_data):
                    self.ct_table.setItem(r, c, QTableWidgetItem(str(data)))

            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def them_don_hang(self):
        try:
            ma = self.dh_ma.text().strip()
            makh = self.dh_makh.text().strip()
            if not ma or not makh:
                raise ValueError("Vui lòng nhập mã đơn và mã khách hàng.")
            if self.order_exists(ma):
                raise ValueError(f"Mã đơn '{ma}' đã tồn tại! Vui lòng nhập mã khác.")
            if not self.customer_exists(makh):
                raise ValueError(f"Mã khách hàng '{makh}' không tồn tại!")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO DonHang (MaDon, MaKH, Ngay) VALUES (?, ?, GETDATE())",
                (ma, makh)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Thành công", f"Thêm đơn hàng '{ma}' thành công!")
            self.clear_don_form()
            self.load_don_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def sua_don_hang(self):
        try:
            ma = self.dh_ma.text().strip()
            makh = self.dh_makh.text().strip()
            if not ma:
                raise ValueError("Chọn hoặc nhập mã đơn hàng để sửa.")
            if not makh:
                raise ValueError("Vui lòng nhập mã khách hàng.")
            if not self.order_exists(ma):
                raise ValueError(f"Đơn hàng '{ma}' không tồn tại.")
            if not self.customer_exists(makh):
                raise ValueError(f"Mã khách hàng '{makh}' không tồn tại!")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE DonHang SET MaKH = ? WHERE MaDon = ?",
                (makh, ma)
            )
            conn.commit()
            conn.close()
            self.load_don_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def xoa_don_hang(self):
        try:
            ma = self.dh_ma.text().strip()
            if not ma:
                raise ValueError("Chọn đơn hàng để xóa.")
            if not self.order_exists(ma):
                raise ValueError(f"Đơn hàng '{ma}' không tồn tại.")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ChiTietDonHang WHERE MaDon = ?", (ma,))
            cursor.execute("DELETE FROM DonHang WHERE MaDon = ?", (ma,))
            conn.commit()
            conn.close()

            self.clear_don_form()
            self.clear_chi_tiet_form()
            self.ct_table.setRowCount(0)
            self.load_don_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def select_don_hang(self):
        items = self.dh_table.selectedItems()
        if not items:
            return
        self.dh_ma.setText(items[0].text())
        self.dh_makh.setText(items[1].text())
        self.load_order_details(items[0].text())

    def tim_don_hang(self):
        self.load_don_hang(self.dh_search.text().strip())

    def them_chi_tiet(self):
        try:
            ma_don = self.dh_ma.text().strip()
            if not ma_don:
                current_row = self.dh_table.currentRow()
                if current_row >= 0 and self.dh_table.item(current_row, 0):
                    ma_don = self.dh_table.item(current_row, 0).text().strip()

            ma_hang = self.ct_mahang.text().strip()
            soluong_text = self.ct_soluong.text().strip()
            dongia_text = self.ct_dongia.text().strip()

            if not ma_don:
                raise ValueError("Chọn đơn hàng trước khi thêm mặt hàng.")
            if not ma_hang or not soluong_text or not dongia_text:
                raise ValueError("Nhập đầy đủ Mã hàng, Số lượng, Đơn giá.")

            try:
                soluong = int(soluong_text)
                dongia = float(dongia_text)
            except ValueError:
                raise ValueError("Số lượng phải là số nguyên, Đơn giá phải là số thực")

            if not self.order_exists(ma_don):
                raise ValueError(f"Hóa đơn {ma_don} không tồn tại!")
            if not self.product_exists(ma_hang):
                raise ValueError(f"Mã mặt hàng '{ma_hang}' không tồn tại!")
            if self.detail_exists(ma_don, ma_hang):
                raise ValueError(f"Mặt hàng '{ma_hang}' đã có trong hóa đơn này! Vui lòng thêm mặt hàng khác.")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ChiTietDonHang (MaDon, MaHang, SoLuong, DonGia) VALUES (?, ?, ?, ?)",
                (ma_don, ma_hang, soluong, dongia)
            )
            conn.commit()
            conn.close()

            self.clear_chi_tiet_form()
            self.load_don_hang()
            self.load_order_details(ma_don)
            QMessageBox.information(self, "Thành công", "Thêm mặt hàng vào hóa đơn thành công!")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def xoa_chi_tiet(self):
        try:
            ma_don = self.dh_ma.text().strip()
            if not ma_don:
                current_row = self.dh_table.currentRow()
                if current_row >= 0 and self.dh_table.item(current_row, 0):
                    ma_don = self.dh_table.item(current_row, 0).text().strip()

            ma_hang = self.ct_mahang.text().strip()

            if not ma_don:
                raise ValueError("Chọn đơn hàng trước khi xóa mặt hàng.")
            if not ma_hang:
                raise ValueError("Nhập mã mặt hàng để xóa.")
            if not self.order_exists(ma_don):
                raise ValueError(f"Đơn hàng '{ma_don}' không tồn tại.")
            if not self.detail_exists(ma_don, ma_hang):
                raise ValueError(f"Mặt hàng '{ma_hang}' không tồn tại trong đơn hàng này.")

            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM ChiTietDonHang WHERE MaDon = ? AND MaHang = ?",
                (ma_don, ma_hang)
            )
            conn.commit()
            conn.close()

            self.clear_chi_tiet_form()
            self.load_order_details(ma_don)
            self.load_don_hang()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def click_don(self, row, col):
        if row < 0:
            return
        item = self.dh_table.item(row, 0)
        if item:
            self.load_order_details(item.text())

# ====== RUN ======
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())