import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Kiểm tra nếu chạy với --gui
if len(sys.argv) > 1 and sys.argv[1] == "--gui":
    try:
        import tkinter as tk
        from gui import EmployeeManagementGUI
        root = tk.Tk()
        app = EmployeeManagementGUI(root)
        root.mainloop()
        sys.exit(0)
    except ImportError:
        print("Tkinter không khả dụng. Chạy chế độ console.")
    except Exception as e:
        print(f"Lỗi GUI: {e}. Chạy chế độ console.")

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



def prompt_with_validation(prompt, validator):
    while True:
        value = input(prompt)
        try:
            return validator(value)
        except ValueError as e:
            print(f"Lỗi đầu vào: {e}")
        except EmployeeException as e:
            print(f"Lỗi: {e}")


def validate_score(value):
    try:
        score = float(value)
    except (ValueError, TypeError):
        raise ValueError("Điểm hiệu suất phải là số")
    if not (0 <= score <= 10):
        raise ValueError("Điểm hiệu suất phải từ 0 đến 10")
    return score


def choose_mode():
    print("Chọn chế độ:")
    print("1. Console (dòng lệnh)")
    print("2. GUI (giao diện đồ họa)")
    while True:
        choice = input("Nhập lựa chọn (1 hoặc 2): ").strip()
        if choice == '1':
            return 'console'
        elif choice == '2':
            return 'gui'
        else:
            print("Lựa chọn không hợp lệ. Nhập 1 hoặc 2.")


def main():
    mode = choose_mode()
    if mode == 'gui':
        try:
            import tkinter as tk
            from gui import EmployeeManagementGUI
            root = tk.Tk()
            app = EmployeeManagementGUI(root)
            root.mainloop()
            return
        except ImportError:
            print("Tkinter không khả dụng. Chuyển sang chế độ console.")
        except Exception as e:
            print(f"Lỗi GUI: {e}. Chuyển sang chế độ console.")

    # Chế độ console
    company = Company()

    while True:
        print(format_form_header("HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ABC"))
        print("1. Thêm nhân viên mới")
        print("2. Hiển thị danh sách nhân viên")
        print("3. Tìm kiếm nhân viên")
        print("4. Quản lý lương")
        print("5. Quản lý dự án")
        print("6. Đánh giá hiệu suất")
        print("7. Quản lý nhân sự")
        print("8. Thống kê báo cáo")
        print("9. Thoát")

        choice = input("Chọn chức năng (1-9): ").strip()

        try:
            if choice == '1':
                add_employee_menu(company)
            elif choice == '2':
                display_menu(company)
            elif choice == '3':
                search_menu(company)
            elif choice == '4':
                salary_menu(company)
            elif choice == '5':
                project_menu(company)
            elif choice == '6':
                performance_menu(company)
            elif choice == '7':
                hr_menu(company)
            elif choice == '8':
                report_menu(company)
            elif choice == '9':
                print("Tạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ!")
        except EmployeeException as e:
            print(f"Lỗi: {e}")
        except IndexError:
            print("Chưa có dữ liệu")
        except ValueError as e:
            print(f"Lỗi đầu vào: {e}")
        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")


def add_employee_menu(company):
    print(format_form_header("THÊM NHÂN VIÊN MỚI"))
    print("a. Thêm Manager")
    print("b. Thêm Developer")
    print("c. Thêm Intern")
    choice = input("Chọn loại (a-c): ").strip().lower()

    emp_id = prompt_with_validation("ID nhân viên: ", validate_employee_id)
    name = prompt_with_validation("Tên: ", validate_name)
    email = prompt_with_validation("Email: ", validate_email)
    age = prompt_with_validation("Tuổi: ", validate_age)
    salary = prompt_with_validation("Lương cơ bản: ", validate_salary)

    if choice == 'a':
        bonus = prompt_with_validation("Thưởng: ", validate_salary)
        emp = Manager(emp_id, name, age, salary, email, bonus)
    elif choice == 'b':
        lang = prompt_with_validation("Ngôn ngữ lập trình: ", validate_name)
        emp = Developer(emp_id, name, age, salary, email, lang)
    elif choice == 'c':
        duration = prompt_with_validation("Thời gian thực tập (tháng): ", lambda v: validate_positive_int(v, "Thời gian thực tập phải là số nguyên"))
        emp = Intern(emp_id, name, age, salary, email, duration)
    else:
        raise ValueError("Lựa chọn loại nhân viên không hợp lệ")

    new_id = company.add_employee(emp)
    if new_id != emp_id:
        print(f"ID trùng, đã tự động đổi thành ID mới: {new_id}")
    print("Thêm nhân viên thành công!")


def display_menu(company):
    print(format_form_header("HIỂN THỊ DANH SÁCH NHÂN VIÊN"))
    print("a. Tất cả nhân viên")
    print("b. Theo loại (Manager/Developer/Intern)")
    print("c. Theo hiệu suất (từ cao đến thấp)")
    choice = input("Chọn (a-c): ").strip().lower()

    if choice == 'a':
        print(format_employee_list(company.ensure_employees(), "Tất cả nhân viên"))
    elif choice == 'b':
        position = input("Chọn loại nhân viên: ").strip()
        emps = [emp for emp in company.ensure_employees() if emp.position.lower() == position.lower()]
        print(format_employee_list(emps, f"Nhân viên theo loại: {position}"))
    elif choice == 'c':
        emps = company.get_employees_by_performance(descending=True)
        if not emps:
            raise IndexError
        print(format_employee_list(emps, "Nhân viên theo hiệu suất"))
    else:
        print("Lựa chọn không hợp lệ!")


def search_menu(company):
    print(format_form_header("TÌM KIẾM NHÂN VIÊN"))
    print("a. Theo ID")
    print("b. Theo tên")
    print("c. Theo ngôn ngữ lập trình (cho Developer)")
    choice = input("Chọn (a-c): ").strip().lower()

    if choice == 'a':
        emp_id = validate_employee_id(input("ID nhân viên: "))
        print(format_employee_info(company.get_employee(emp_id)))
    elif choice == 'b':
        name = validate_name(input("Tên hoặc một phần tên: "))
        results = company.search_by_name(name)
        print(format_employee_list(results, f"Kết quả tìm theo tên: {name}"))
    elif choice == 'c':
        language = validate_name(input("Ngôn ngữ lập trình: "))
        results = company.search_by_language(language)
        print(format_employee_list(results, f"Developer theo ngôn ngữ: {language}"))
    else:
        print("Lựa chọn không hợp lệ!")


def salary_menu(company):
    print(format_form_header("QUẢN LÝ LƯƠNG"))
    print("a. Tính lương cho từng nhân viên")
    print("b. Tính tổng lương công ty")
    print("c. Top 3 nhân viên lương cao nhất")
    choice = input("Chọn (a-c): ").strip().lower()

    if choice == 'a':
        emp_id = validate_employee_id(input("ID nhân viên: "))
        salary = calculate_salary_for_employee(company, emp_id)
        print(f"Lương của nhân viên {emp_id}: {salary:,.0f} VND")
    elif choice == 'b':
        company.ensure_employees()
        total_payroll = calculate_total_payroll(company)
        stats = get_salary_statistics(company)
        print(format_payroll_summary(total_payroll, stats))
    elif choice == 'c':
        top_emps = get_top_n_earners(company, 3)
        if not top_emps:
            raise IndexError
        print(format_employee_list(top_emps, "Top 3 nhân viên lương cao nhất"))
    else:
        print("Lựa chọn không hợp lệ!")


def project_menu(company):
    print(format_form_header("QUẢN LÝ DỰ ÁN"))
    print("a. Phân công nhân viên vào dự án")
    print("b. Xóa nhân viên khỏi dự án")
    print("c. Hiển thị dự án của nhân viên")
    choice = input("Chọn (a-c): ").strip().lower()

    if choice == 'a':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên: "))
        project = validate_name(input("Tên dự án: "))
        company.assign_project_to_employee(emp_id, project)
        print("Phân công dự án thành công!")
    elif choice == 'b':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên: "))
        project = validate_name(input("Tên dự án cần xóa: "))
        company.remove_project_from_employee(emp_id, project)
        print("Xóa nhân viên khỏi dự án thành công!")
    elif choice == 'c':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên: "))
        projects = company.get_employee_projects(emp_id)
        print(f"Danh sách dự án của {emp_id}: {', '.join(projects) if projects else 'Không có dự án'}")
    else:
        print("Lựa chọn không hợp lệ!")


def performance_menu(company):
    print(format_form_header("ĐÁNH GIÁ HIỆU SUẤT"))
    print("a. Cập nhật điểm hiệu suất cho nhân viên")
    print("b. Hiển thị nhân viên xuất sắc (điểm > 8)")
    print("c. Hiển thị nhân viên cần cải thiện (điểm < 5)")
    choice = input("Chọn (a-c): ").strip().lower()

    if choice == 'a':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên: "))
        score = prompt_with_validation("Điểm hiệu suất (0-10): ", validate_score)
        company.evaluate_employee(emp_id, score)
        print("Cập nhật hiệu suất thành công!")
    elif choice == 'b':
        excellent = company.get_employees_by_performance(min_score=8.1)
        if not excellent:
            raise IndexError
        print(format_employee_list(excellent, "Nhân viên xuất sắc"))
    elif choice == 'c':
        needs_improve = company.get_employees_by_performance(max_score=4.9)
        if not needs_improve:
            raise IndexError
        print(format_employee_list(needs_improve, "Nhân viên cần cải thiện"))
    else:
        print("Lựa chọn không hợp lệ!")


def hr_menu(company):
    print(format_form_header("QUẢN LÝ NHÂN SỰ"))
    print("a. Nghỉ việc nhân viên")
    print("b. Tăng lương cơ bản cho nhân viên")
    print("c. Thăng chức nhân viên")
    print("d. Giảm lương nhân viên")
    choice = input("Chọn (a-d): ").strip().lower()

    if choice == 'a':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên nghỉ việc: "))
        compensation_months = prompt_with_validation("Số tháng đền bù hợp đồng (0 nếu không có): ", lambda v: validate_positive_int(v, "Số tháng phải là số nguyên"))
        amount = company.terminate_employee(emp_id, compensation_months)
        print(f"Nhân viên đã nghỉ việc. Tổng đền bù: {amount:,.0f} VND")
    elif choice == 'b':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên: "))
        amount = validate_salary(input("Số tiền tăng lương: "))
        company.increase_salary(emp_id, amount)
        print("Tăng lương cơ bản thành công!")
    elif choice == 'c':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên muốn thăng chức: "))
        company.promote_employee(emp_id)
        print("Thăng chức thành công!")
    elif choice == 'd':
        company.ensure_employees()
        emp_id = validate_employee_id(input("ID nhân viên: "))
        amount = validate_salary(input("Số tiền giảm lương: "))
        company.decrease_salary(emp_id, amount)
        print("Giảm lương nhân viên thành công!")
    else:
        print("Lựa chọn không hợp lệ!")


def report_menu(company):
    print(format_form_header("THỐNG KÊ BÁO CÁO"))
    print("a. Số lượng nhân viên theo loại")
    print("b. Tổng lương theo chức vụ")
    print("c. Số dự án trung bình trên mỗi nhân viên")
    print("d. Sắp xếp nhân viên theo số dự án (từ nhiều đến ít)")
    choice = input("Chọn (a-d): ").strip().lower()

    if choice == 'a':
        report = company.count_by_position()
        if not report:
            raise IndexError
        print(format_report_summary(report))
    elif choice == 'b':
        report = company.total_salary_by_position()
        if not report:
            raise IndexError
        print(format_report_summary(report))
    elif choice == 'c':
        company.ensure_employees()
        average = company.average_projects_per_employee()
        print(f"Số dự án trung bình trên mỗi nhân viên: {average:.2f}")
    elif choice == 'd':
        emps = company.sort_by_project_count()
        if not emps:
            raise IndexError
        print(format_employee_list(emps, "Nhân viên theo số dự án"))
    else:
        print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()