import pytest
from classes import Employee
from functions import add


@pytest.mark.parametrize("name, age, salary, expected", [
    ("John", 30, 50000, "John"),
    ("Jane", 25, 50000, "Jane"),
    (-1, 30, 50000, -1),
])
def test_employee_creation(name, age, salary, expected):
    employee = Employee(name, age, salary)
    assert employee.name == expected

@pytest.mark.parametrize("x, y, expected", [
    (("x", 1), 2, 3),
    (("x", 0), 0, 0),
    (("x", -1), 1, 0),
])
def test_add_fx(x, y, expected):
    assert add(x[1], y) == expected


