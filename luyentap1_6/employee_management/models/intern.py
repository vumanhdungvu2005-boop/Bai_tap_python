from .employee import Employee

class Intern(Employee):
    def __init__(self, employee_id, name, age, base_salary, email, internship_duration=6):
        super().__init__(employee_id, name, age, base_salary, "Intern", email)
        self.internship_duration = internship_duration  # Tháng

    def calculate_salary(self):
        return self.base_salary + (self.performance_score * 20000)