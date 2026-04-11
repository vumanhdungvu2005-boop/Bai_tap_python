def format_employee_info(employee):
    return f"""
ID: {employee.employee_id}
Tên: {employee.name}
Tuổi: {employee.age}
Chức vụ: {employee.position}
Lương: {employee.calculate_salary():,.0f} VND
Dự án: {', '.join(employee.projects) if employee.projects else 'Không có'}
Điểm hiệu suất: {employee.performance_score}
"""

def format_form_header(title):
    border = "=" * (len(title) + 8)
    return f"\n{border}\n  {title}  \n{border}\n"

def format_employee_info(employee):
    return f"""
ID: {employee.employee_id}
Tên: {employee.name}
Tuổi: {employee.age}
Chức vụ: {employee.position}
Trạng thái: {employee.employment_status}
Lương cơ bản: {employee.base_salary:,.0f} VND
Lương thực nhận: {employee.calculate_salary():,.0f} VND
Dự án: {', '.join(employee.projects) if employee.projects else 'Không có'}
Điểm hiệu suất: {employee.performance_score}
"""

def format_employee_brief(employee):
    projects = len(employee.projects)
    return f"ID={employee.employee_id} | {employee.name} | {employee.position} | Lương={employee.calculate_salary():,.0f} | Hiệu suất={employee.performance_score} | Dự án={projects}"

def format_employee_list(employees, title=None):
    content = ""
    if title:
        content += format_form_header(title)
    if not employees:
        return content + "Không tìm thấy nhân viên nào.\n"
    for emp in employees:
        content += format_employee_brief(emp) + "\n"
    return content

def format_payroll_summary(total, stats):
    return f"""
Tổng lương: {total:,.0f} VND
Lương thấp nhất: {stats['min']:,.0f} VND
Lương cao nhất: {stats['max']:,.0f} VND
Lương trung bình: {stats['avg']:,.0f} VND
"""

def format_report_summary(report):
    lines = []
    for key, value in report.items():
        if isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"