import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from employee_management.services.company import Company
from employee_management.services.payroll import (
    calculate_total_payroll,
    get_salary_statistics,
    get_top_n_earners,
    calculate_salary_for_employee,
)
from employee_management.models import Manager, Developer, Intern
from employee_management.utils.validators import (
    validate_employee_id,
    validate_name,
    validate_email,
    validate_age,
    validate_salary,
    validate_positive_int,
)
from employee_management.utils.formatters import (
    format_employee_info,
    format_employee_list,
    format_payroll_summary,
    format_form_header,
    format_report_summary,
)
from employee_management.exceptions.employee_exceptions import EmployeeException


class EmployeeManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống quản lý nhân viên công ty ABC")
        self.root.geometry("800x600")

        self.company = Company()

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Employee menu
        emp_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nhân viên", menu=emp_menu)
        emp_menu.add_command(label="Thêm nhân viên", command=self.add_employee_gui)
        emp_menu.add_command(label="Hiển thị nhân viên", command=self.display_employees_gui)
        emp_menu.add_command(label="Tìm kiếm nhân viên", command=self.search_employee_gui)

        # Project menu
        proj_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dự án", menu=proj_menu)
        proj_menu.add_command(label="Phân công dự án", command=self.assign_project_gui)
        proj_menu.add_command(label="Xóa dự án", command=self.remove_project_gui)

        # Salary menu
        salary_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Lương", menu=salary_menu)
        salary_menu.add_command(label="Tính lương nhân viên", command=self.calculate_salary_gui)
        salary_menu.add_command(label="Tổng lương công ty", command=self.total_payroll_gui)

        # Performance menu
        perf_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hiệu suất", menu=perf_menu)
        perf_menu.add_command(label="Đánh giá hiệu suất", command=self.evaluate_performance_gui)

        # HR menu
        hr_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nhân sự", menu=hr_menu)
        hr_menu.add_command(label="Nghỉ việc", command=self.terminate_employee_gui)
        hr_menu.add_command(label="Tăng lương", command=self.increase_salary_gui)
        hr_menu.add_command(label="Thăng chức", command=self.promote_employee_gui)

        # Report menu
        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Báo cáo", menu=report_menu)
        report_menu.add_command(label="Thống kê", command=self.report_gui)

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.display_welcome()

    def display_welcome(self):
        self.text_area.delete(1.0, tk.END)
        welcome_text = """
=== HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ABC ===

Chào mừng bạn đến với hệ thống quản lý nhân viên!

Sử dụng menu trên để thực hiện các chức năng:
- Thêm, hiển thị, tìm kiếm nhân viên
- Quản lý dự án và lương
- Đánh giá hiệu suất
- Quản lý nhân sự
- Báo cáo thống kê

Bắt đầu bằng cách chọn một chức năng từ menu.
"""
        self.text_area.insert(tk.END, welcome_text)

    def add_employee_gui(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm nhân viên")
        dialog.geometry("400x500")

        tk.Label(dialog, text="Loại nhân viên:").pack()
        emp_type_var = tk.StringVar(value="Manager")
        tk.OptionMenu(dialog, emp_type_var, "Manager", "Developer", "Intern").pack()

        tk.Label(dialog, text="ID nhân viên:").pack()
        emp_id_entry = tk.Entry(dialog)
        emp_id_entry.pack()

        tk.Label(dialog, text="Tên:").pack()
        name_entry = tk.Entry(dialog)
        name_entry.pack()

        tk.Label(dialog, text="Email:").pack()
        email_entry = tk.Entry(dialog)
        email_entry.pack()

        tk.Label(dialog, text="Tuổi:").pack()
        age_entry = tk.Entry(dialog)
        age_entry.pack()

        tk.Label(dialog, text="Lương cơ bản:").pack()
        salary_entry = tk.Entry(dialog)
        salary_entry.pack()

        bonus_frame = tk.Frame(dialog)
        tk.Label(bonus_frame, text="Thưởng (cho Manager):").pack(side=tk.LEFT)
        bonus_entry = tk.Entry(bonus_frame)
        bonus_entry.pack(side=tk.LEFT)
        bonus_frame.pack()

        lang_frame = tk.Frame(dialog)
        tk.Label(lang_frame, text="Ngôn ngữ lập trình (cho Developer):").pack(side=tk.LEFT)
        lang_entry = tk.Entry(lang_frame)
        lang_entry.pack(side=tk.LEFT)
        lang_frame.pack()

        duration_frame = tk.Frame(dialog)
        tk.Label(duration_frame, text="Thời gian thực tập (tháng, cho Intern):").pack(side=tk.LEFT)
        duration_entry = tk.Entry(duration_frame)
        duration_entry.pack(side=tk.LEFT)
        duration_frame.pack()

        def submit():
            try:
                emp_type = emp_type_var.get()
                emp_id = validate_employee_id(emp_id_entry.get())
                name = validate_name(name_entry.get())
                email = validate_email(email_entry.get())
                age = validate_age(age_entry.get())
                salary = validate_salary(salary_entry.get())

                if emp_type == "Manager":
                    bonus = validate_salary(bonus_entry.get())
                    emp = Manager(emp_id, name, age, salary, email, bonus)
                elif emp_type == "Developer":
                    lang = validate_name(lang_entry.get())
                    emp = Developer(emp_id, name, age, salary, email, lang)
                elif emp_type == "Intern":
                    duration = validate_positive_int(duration_entry.get(), "Thời gian thực tập phải là số nguyên")
                    emp = Intern(emp_id, name, age, salary, email, duration)

                new_id = self.company.add_employee(emp)
                if new_id != emp_id:
                    messagebox.showinfo("Thành công", f"ID trùng, đã tự động đổi thành ID mới: {new_id}")
                else:
                    messagebox.showinfo("Thành công", "Thêm nhân viên thành công!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        tk.Button(dialog, text="Thêm", command=submit).pack()
        tk.Button(dialog, text="Hủy", command=dialog.destroy).pack()

    def display_employees_gui(self):
        self.text_area.delete(1.0, tk.END)
        try:
            employees = self.company.ensure_employees()
            self.text_area.insert(tk.END, format_employee_list(employees, "Danh sách nhân viên"))
        except IndexError:
            self.text_area.insert(tk.END, "Chưa có dữ liệu")

    def search_employee_gui(self):
        emp_id = simpledialog.askstring("Tìm kiếm", "Nhập ID nhân viên:")
        if emp_id:
            try:
                emp = self.company.get_employee(validate_employee_id(emp_id))
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, format_employee_info(emp))
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def assign_project_gui(self):
        emp_id = simpledialog.askstring("Phân công dự án", "ID nhân viên:")
        if emp_id:
            project = simpledialog.askstring("Phân công dự án", "Tên dự án:")
            if project:
                try:
                    self.company.ensure_employees()
                    self.company.assign_project_to_employee(validate_employee_id(emp_id), validate_name(project))
                    messagebox.showinfo("Thành công", "Phân công dự án thành công!")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))

    def remove_project_gui(self):
        emp_id = simpledialog.askstring("Xóa dự án", "ID nhân viên:")
        if emp_id:
            project = simpledialog.askstring("Xóa dự án", "Tên dự án:")
            if project:
                try:
                    self.company.ensure_employees()
                    self.company.remove_project_from_employee(validate_employee_id(emp_id), validate_name(project))
                    messagebox.showinfo("Thành công", "Xóa dự án thành công!")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))

    def calculate_salary_gui(self):
        emp_id = simpledialog.askstring("Tính lương", "ID nhân viên:")
        if emp_id:
            try:
                salary = calculate_salary_for_employee(self.company, validate_employee_id(emp_id))
                messagebox.showinfo("Lương", f"Lương của nhân viên {emp_id}: {salary:,.0f} VND")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def total_payroll_gui(self):
        try:
            self.company.ensure_employees()
            total = calculate_total_payroll(self.company)
            stats = get_salary_statistics(self.company)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, format_payroll_summary(total, stats))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def evaluate_performance_gui(self):
        emp_id = simpledialog.askstring("Đánh giá hiệu suất", "ID nhân viên:")
        if emp_id:
            score = simpledialog.askfloat("Đánh giá hiệu suất", "Điểm (0-10):")
            if score is not None:
                try:
                    self.company.ensure_employees()
                    self.company.evaluate_employee(validate_employee_id(emp_id), score)
                    messagebox.showinfo("Thành công", "Đánh giá thành công!")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))

    def terminate_employee_gui(self):
        emp_id = simpledialog.askstring("Nghỉ việc", "ID nhân viên:")
        if emp_id:
            months = simpledialog.askinteger("Nghỉ việc", "Số tháng đền bù:")
            if months is not None:
                try:
                    self.company.ensure_employees()
                    amount = self.company.terminate_employee(validate_employee_id(emp_id), months)
                    messagebox.showinfo("Thành công", f"Nhân viên đã nghỉ việc. Đền bù: {amount:,.0f} VND")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))

    def increase_salary_gui(self):
        emp_id = simpledialog.askstring("Tăng lương", "ID nhân viên:")
        if emp_id:
            amount = simpledialog.askfloat("Tăng lương", "Số tiền:")
            if amount is not None:
                try:
                    self.company.ensure_employees()
                    self.company.increase_salary(validate_employee_id(emp_id), validate_salary(str(amount)))
                    messagebox.showinfo("Thành công", "Tăng lương thành công!")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))

    def promote_employee_gui(self):
        emp_id = simpledialog.askstring("Thăng chức", "ID nhân viên:")
        if emp_id:
            try:
                self.company.ensure_employees()
                self.company.promote_employee(validate_employee_id(emp_id))
                messagebox.showinfo("Thành công", "Thăng chức thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def report_gui(self):
        self.text_area.delete(1.0, tk.END)
        try:
            report = self.company.count_by_position()
            if not report:
                raise IndexError
            self.text_area.insert(tk.END, "Số lượng nhân viên theo loại:\n")
            self.text_area.insert(tk.END, format_report_summary(report))
            self.text_area.insert(tk.END, "\n\nTổng lương theo chức vụ:\n")
            salary_report = self.company.total_salary_by_position()
            self.text_area.insert(tk.END, format_report_summary(salary_report))
            self.text_area.insert(tk.END, f"\n\nSố dự án trung bình: {self.company.average_projects_per_employee():.2f}")
        except IndexError:
            self.text_area.insert(tk.END, "Chưa có dữ liệu")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementGUI(root)
    root.mainloop()