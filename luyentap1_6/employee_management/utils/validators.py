import re
from ..exceptions.employee_exceptions import InvalidAgeError, InvalidSalaryError

def validate_employee_id(employee_id):
    if not isinstance(employee_id, str) or not employee_id.strip():
        raise ValueError("ID nhân viên phải là chuỗi không rỗng")
    return employee_id.strip()

def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Tên phải là chuỗi không rỗng")
    return name.strip()

def validate_email(email):
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email phải là chuỗi không rỗng")
    email = email.strip()
    if '@' not in email or email.startswith('@') or email.endswith('@'):
        raise ValueError("Email phải chứa ký tự @ và có định dạng hợp lệ")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise ValueError("Email không đúng định dạng")
    return email

def validate_age(age):
    try:
        age = int(age)
    except (ValueError, TypeError):
        raise ValueError("Tuổi phải là số nguyên")
    if not (18 <= age <= 65):
        raise InvalidAgeError("Tuổi phải từ 18 đến 65")
    return age

def validate_salary(salary):
    try:
        salary = float(salary)
    except (ValueError, TypeError):
        raise ValueError("Lương phải là số")
    if salary <= 0:
        raise InvalidSalaryError("Lương phải lớn hơn 0")
    return salary

def validate_positive_int(value, message):
    try:
        result = int(value)
    except (ValueError, TypeError):
        raise ValueError(message)
    return result