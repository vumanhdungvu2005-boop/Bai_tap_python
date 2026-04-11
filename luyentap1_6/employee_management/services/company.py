from ..models import Employee, Manager, Developer, Intern
from ..exceptions.employee_exceptions import EmployeeNotFoundError, DuplicateEmployeeError, EmployeeException

class Company:
    def __init__(self):
        self.employees = {}

    def _generate_unique_id(self, employee_id):
        if employee_id not in self.employees:
            return employee_id
        base = employee_id
        suffix = 1
        while f"{base}_{suffix}" in self.employees:
            suffix += 1
        return f"{base}_{suffix}"

    def add_employee(self, employee):
        if employee.employee_id in self.employees:
            new_id = self._generate_unique_id(employee.employee_id)
            employee.employee_id = new_id
            self.employees[new_id] = employee
            return new_id
        self.employees[employee.employee_id] = employee
        return employee.employee_id

    def get_employee(self, employee_id):
        if employee_id not in self.employees:
            raise EmployeeNotFoundError(employee_id)
        return self.employees[employee_id]

    def list_employees(self, active_only=True):
        if active_only:
            return [emp for emp in self.employees.values() if emp.is_active()]
        return list(self.employees.values())

    def ensure_employees(self, active_only=True):
        employees = self.list_employees(active_only=active_only)
        if not employees:
            raise IndexError("Chưa có dữ liệu")
        return employees

    def remove_employee(self, employee_id):
        employee = self.get_employee(employee_id)
        employee.terminate()

    def assign_project_to_employee(self, employee_id, project_name):
        employee = self.get_employee(employee_id)
        if not employee.is_active():
            raise EmployeeException("Không thể phân công dự án cho nhân viên đã nghỉ việc")
        employee.assign_project(project_name)

    def remove_project_from_employee(self, employee_id, project_name):
        employee = self.get_employee(employee_id)
        employee.remove_project(project_name)

    def get_employee_projects(self, employee_id):
        employee = self.get_employee(employee_id)
        return employee.projects

    def evaluate_employee(self, employee_id, score):
        employee = self.get_employee(employee_id)
        if not employee.is_active():
            raise EmployeeException("Không thể đánh giá nhân viên đã nghỉ việc")
        employee.evaluate_performance(score)

    def search_by_name(self, name):
        return [emp for emp in self.list_employees() if name.lower() in emp.name.lower()]

    def search_by_language(self, language):
        return [emp for emp in self.list_employees() if isinstance(emp, Developer) and language.lower() in emp.programming_language.lower()]

    def get_top_earners(self, top_n=3):
        return sorted(self.list_employees(), key=lambda emp: emp.calculate_salary(), reverse=True)[:top_n]

    def get_employees_by_performance(self, min_score=None, max_score=None, descending=True):
        employees = self.list_employees()
        if min_score is not None:
            employees = [emp for emp in employees if emp.performance_score >= min_score]
        if max_score is not None:
            employees = [emp for emp in employees if emp.performance_score <= max_score]
        return sorted(employees, key=lambda emp: emp.performance_score, reverse=descending)

    def count_by_position(self):
        report = {}
        for emp in self.list_employees():
            report[emp.position] = report.get(emp.position, 0) + 1
        return report

    def total_salary_by_position(self):
        report = {}
        for emp in self.list_employees():
            report[emp.position] = report.get(emp.position, 0) + emp.calculate_salary()
        return report

    def average_projects_per_employee(self):
        employees = self.list_employees()
        if not employees:
            return 0
        return sum(emp.get_project_count() for emp in employees) / len(employees)

    def sort_by_project_count(self, descending=True):
        return sorted(self.list_employees(), key=lambda emp: emp.get_project_count(), reverse=descending)

    def increase_salary(self, employee_id, amount):
        employee = self.get_employee(employee_id)
        if not employee.is_active():
            raise EmployeeException("Không thể tăng lương cho nhân viên đã nghỉ việc")
        employee.increase_salary(amount)

    def decrease_salary(self, employee_id, amount):
        employee = self.get_employee(employee_id)
        if not employee.is_active():
            raise EmployeeException("Không thể giảm lương cho nhân viên đã nghỉ việc")
        employee.decrease_salary(amount)

    def promote_employee(self, employee_id):
        employee = self.get_employee(employee_id)
        if not employee.is_active():
            raise EmployeeException("Không thể thăng chức nhân viên đã nghỉ việc")
        if isinstance(employee, Intern):
            promoted = Developer(
                employee.employee_id,
                employee.name,
                employee.age,
                employee.base_salary,
                employee.email,
                programming_language="Python",
            )
        elif isinstance(employee, Developer):
            promoted = Manager(
                employee.employee_id,
                employee.name,
                employee.age,
                employee.base_salary,
                employee.email,
                bonus=0,
            )
        else:
            raise EmployeeException("Nhân viên hiện tại không thể thăng chức thêm")
        promoted.projects = employee.projects.copy()
        promoted.performance_score = employee.performance_score
        self.employees[employee_id] = promoted

    def terminate_employee(self, employee_id, compensation_months=0):
        employee = self.get_employee(employee_id)
        if not employee.is_active():
            raise EmployeeException("Nhân viên đã được nghỉ trước đó")
        employee.terminate()
        return employee.base_salary * compensation_months