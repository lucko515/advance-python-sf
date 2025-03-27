import pytest
import unittest
from classes import Employee
from functions import add

@pytest.mark.parametrize("a, b, expected",[
    (2, 2, 4),
    (1, -1, 0),
    (10, 0, 10)
])
def test_add(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("name, age, salary, expected", [
    ("John", 30, 50000, "John"),
    ("Mark", 30, 50000, "Mark"),
])
def test_employee_creation(name, age, salary, expected):
    employee = Employee(name, age, salary) 
    assert employee.name == expected

class TestEmployeeParametrized(unittest.TestCase):

    def test_employee_creation(self):

        test_case = [
            ("John", 30, 50000, "John"),
            ("Mark", 30, 50000, "24"),
        ]

        for name, age, salary, expected in test_case:
            with self.subTest(name=name, age=age, salary=salary, expected=expected):
                employee = Employee(name, age, salary)
                self.assertEqual(employee.name, expected)


if __name__ == "__main__":
    unittest.main()