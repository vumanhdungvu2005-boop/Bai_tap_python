import sys
import pyodbc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, Qt
# from gt import Ui_App
# ===== KẾT NỐI SQL SERVER =====
def connect():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=MANH-DUNG-VU\\SQLEXPRESS03;"
        "DATABASE=QuanLyNhanSu;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

# ===== UI =====
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý nhân sự")
        self.setGeometry(200, 100, 950, 600)

        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #eef4fb, stop:1 #f8fbff);
            }
            QLabel#titleLabel {
                font-size: 26px;
                font-weight: 700;
                color: #2a4a6b;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 10px;
                border: 1px solid #cbd6e2;
                border-radius: 12px;
                background: white;
            }
            QComboBox { min-height: 36px; }
            QPushButton {
                background-color: #1877d2;
                color: white;
                padding: 10px;
                border-radius: 12px;
                min-width: 100px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #145db3;
            }
            QPushButton#deleteButton { background-color: #d64545; }
            QPushButton#deleteButton:hover { background-color: #b63e3e; }
            QPushButton#showButton { background-color: #ff8c00; }
            QPushButton#showButton:hover { background-color: #e07d00; }
            QTableWidget {
                border: 1px solid #cbd6e2;
                border-radius: 14px;
                gridline-color: #e1e8f0;
                background: white;
            }
            QTableWidget::item:selected {
                background: #dbe9fb;
            }
            QHeaderView::section {
                background-color: #eef4fb;
                padding: 8px;
                border: 1px solid #d2dce6;
                color: #253858;
            }
            QGroupBox {
                border: 1px solid #d4dde8;
                border-radius: 14px;
                margin-top: 15px;
                background: rgba(255,255,255,0.92);
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: #274060;
                font-weight: 700;
            }
        """)

        layout = QVBoxLayout()

        title_label = QLabel("Quản lý nhân sự")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # ===== INPUT =====
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        self.cccd = QLineEdit(); self.cccd.setPlaceholderText("Nhập CCCD")
        self.ten = QLineEdit(); self.ten.setPlaceholderText("Nhập họ tên")

        self.ns = QDateEdit()
        self.ns.setCalendarPopup(True)
        self.ns.setDate(QDate.currentDate())

        self.gt = QComboBox()
        self.gt.addItems(["Nam", "Nữ"])
        self.gt.currentTextChanged.connect(self.on_gender_changed)
        self.gt_info = QLabel("Chọn giới tính để hiển thị Nam/Nữ")
        self.gt_info.setStyleSheet("color: #555; font-style: italic;")

        self.dc = QLineEdit(); self.dc.setPlaceholderText("Nhập địa chỉ")

        form_layout.addRow(QLabel("CCCD:"), self.cccd)
        form_layout.addRow(QLabel("Họ tên:"), self.ten)
        form_layout.addRow(QLabel("Ngày sinh:"), self.ns)
        form_layout.addRow(QLabel("Giới tính:"), self.gt)
        form_layout.addRow(QLabel(""), self.gt_info)
        form_layout.addRow(QLabel("Địa chỉ:"), self.dc)

        form_group = QGroupBox("Thông tin nhân sự")
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # ===== BUTTON =====
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        btn_add = QPushButton("Thêm"); btn_add.setObjectName("addButton"); btn_add.clicked.connect(self.them)
        btn_update = QPushButton("Sửa"); btn_update.setObjectName("updateButton"); btn_update.clicked.connect(self.sua)
        btn_delete = QPushButton("Xóa"); btn_delete.setObjectName("deleteButton"); btn_delete.clicked.connect(self.xoa)
        btn_search = QPushButton("Tìm"); btn_search.setObjectName("searchButton"); btn_search.clicked.connect(self.tim)
        btn_show = QPushButton("Hiển thị"); btn_show.setObjectName("showButton"); btn_show.clicked.connect(self.load_data)

        for b in [btn_add, btn_update, btn_delete, btn_search, btn_show]:
            btn_layout.addWidget(b)

        layout.addLayout(btn_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["CCCD", "Họ tên", "Ngày sinh", "Giới tính", "Địa chỉ"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.cellClicked.connect(self.fill_form)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

    # ===== LOAD =====
    def load_data(self):
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nhan_su")
            rows = cursor.fetchall()

            print("Số dòng:", len(rows))  # debug

            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

            conn.close()
        except Exception as e:
            print("Lỗi load:", e)

    # ===== CLICK TABLE =====
    def fill_form(self, row, col):
        self.cccd.setText(self.table.item(row, 0).text())
        self.ten.setText(self.table.item(row, 1).text())
        self.ns.setDate(QDate.fromString(self.table.item(row, 2).text(), "yyyy-MM-dd"))
        self.gt.setCurrentText(self.table.item(row, 3).text())
        self.dc.setText(self.table.item(row, 4).text())

    def on_gender_changed(self, value):
        self.gt_info.setText(f"Giới tính đã chọn: {value}")

    # ===== THÊM =====
    def them(self):
        try:
            conn = connect(); cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO nhan_su VALUES (?, ?, ?, ?, ?)",
                (self.cccd.text(), self.ten.text(), self.ns.date().toString("yyyy-MM-dd"), self.gt.currentText(), self.dc.text())
            )
            conn.commit(); conn.close()
            QMessageBox.information(self, "OK", "Thêm thành công")
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    # ===== SỬA =====
    def sua(self):
        conn = connect(); cursor = conn.cursor()
        cursor.execute("""
        UPDATE nhan_su SET ho_ten=?, ngay_sinh=?, gioi_tinh=?, dia_chi=? WHERE cccd=?
        """, (self.ten.text(), self.ns.date().toString("yyyy-MM-dd"), self.gt.currentText(), self.dc.text(), self.cccd.text()))
        conn.commit(); conn.close()
        QMessageBox.information(self, "OK", "Đã sửa")
        self.load_data()

    # ===== XÓA =====
    def xoa(self):
        conn = connect(); cursor = conn.cursor()
        cursor.execute("DELETE FROM nhan_su WHERE cccd=?", (self.cccd.text(),))
        conn.commit(); conn.close()
        QMessageBox.information(self, "OK", "Đã xóa")
        self.load_data()

    # ===== TÌM =====
    def tim(self):
        key = self.cccd.text()
        conn = connect(); cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM nhan_su
        WHERE cccd LIKE ? OR ho_ten LIKE ? OR dia_chi LIKE ?
        """, ('%'+key+'%', '%'+key+'%', '%'+key+'%'))
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
