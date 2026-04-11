from .company import Company

def calculate_total_payroll(company):
    total = sum(emp.calculate_salary() for emp in company.list_employees())
    return total

def get_salary_statistics(company):
    salaries = [emp.calculate_salary() for emp in company.list_employees()]
    if not salaries:
        return {"min": 0, "max": 0, "avg": 0}
    return {
        "min": min(salaries),
        "max": max(salaries),
        "avg": sum(salaries) / len(salaries)
    }

from .company import Company

def calculate_total_payroll(company):
    total = sum(emp.calculate_salary() for emp in company.list_employees())
    return total

def get_salary_statistics(company):
    salaries = [emp.calculate_salary() for emp in company.list_employees()]
    if not salaries:
        return {"min": 0, "max": 0, "avg": 0}
    return {
        "min": min(salaries),
        "max": max(salaries),
        "avg": sum(salaries) / len(salaries)
    }

def get_employees_by_position(company, position):
    return [emp for emp in company.list_employees() if emp.position.lower() == position.lower()]

def get_top_n_earners(company, n=3):
    return company.get_top_earners(top_n=n)

def calculate_salary_for_employee(company, employee_id):
    employee = company.get_employee(employee_id)
    return employee.calculate_salary()