from .employee import Employee

class Manager(Employee):
    def __init__(self, employee_id, name, age, base_salary, email, bonus=0):
        super().__init__(employee_id, name, age, base_salary, "Manager", email)
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus + (self.performance_score * 100000)