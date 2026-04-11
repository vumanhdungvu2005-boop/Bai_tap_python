from .employee import Employee

class Developer(Employee):
    def __init__(self, employee_id, name, age, base_salary, email, programming_language="Python"):
        super().__init__(employee_id, name, age, base_salary, "Developer", email)
        self.programming_language = programming_language

    def calculate_salary(self):
        return self.base_salary + (self.performance_score * 50000)