# ---- Fixtures ----


import pytest
from classes import Employee


# Fixture employee

def test_employee_creation():
    employee = None
    assert employee.lastname == "Jane"
    assert employee.age == 25
    assert employee.salary == 50000

def test_employee_salary():
    employee = None
    assert employee.get_salary() == 50000

def test_employee_projected_salary():
    employee = None
    assert employee.projected_salary(1) == 52500
    assert employee.projected_salary(0) == 50000



