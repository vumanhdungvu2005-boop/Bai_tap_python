from abc import ABC, abstractmethod
from ..exceptions.employee_exceptions import InvalidAgeError, InvalidSalaryError, ProjectAllocationError

class Employee(ABC):
    def __init__(self, employee_id, name, age, base_salary, position, email):
        if not (18 <= age <= 65):
            raise InvalidAgeError("Tuổi phải từ 18 đến 65")
        if base_salary < 0:
            raise InvalidSalaryError("Lương cơ bản phải lớn hơn 0")
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.base_salary = base_salary
        self.position = position
        self.email = email
        self.projects = []
        self.performance_score = 5.0  # Mặc định trung bình
        self.employment_status = "active"

    @abstractmethod
    def calculate_salary(self):
        """Tính lương theo chức vụ"""
        pass

    def assign_project(self, project_name):
        if project_name in self.projects:
            raise ValueError("Dự án đã được phân công")
        if len(self.projects) >= 5:
            raise ProjectAllocationError("Nhân viên đã có tối đa 5 dự án")
        self.projects.append(project_name)

    def remove_project(self, project_name):
        if project_name not in self.projects:
            raise ValueError("Dự án không tồn tại")
        self.projects.remove(project_name)

    def evaluate_performance(self, score):
        if not (0 <= score <= 10):
            raise ValueError("Điểm hiệu suất phải từ 0 đến 10")
        self.performance_score = score

    def increase_salary(self, amount):
        if amount < 0:
            raise InvalidSalaryError("Số tiền tăng lương phải là số không âm")
        self.base_salary += amount

    def decrease_salary(self, amount):
        if amount < 0:
            raise InvalidSalaryError("Số tiền giảm lương phải là số không âm")
        if self.base_salary - amount < 0:
            raise InvalidSalaryError("Lương không thể giảm xuống dưới 0")
        self.base_salary -= amount

    def terminate(self):
        self.employment_status = "terminated"

    def is_active(self):
        return self.employment_status == "active"

    def get_project_count(self):
        return len(self.projects)

    def __str__(self):
        return f"ID: {self.employee_id}, Tên: {self.name}, Tuổi: {self.age}, Chức vụ: {self.position}, Email: {self.email}, Lương: {self.calculate_salary():,.0f} VND"
