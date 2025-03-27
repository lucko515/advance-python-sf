import pytest
from classes import Person, Employee

class TestPerson:
    
    def test_person_creation(self):
        person = Person("John", 30)
        assert person.name == "John"
        assert person.age == 30

class TestEmployee:

    def setup_method(self):
        self.employee = Employee("Jane", 30, 5000)

    def teardown_method(self):
        del self.employee

    def test_employee_creation(self):
        assert self.employee.name == "Jane"

    def test_employee_projected_salary(self):
        assert self.employee.projected_salary(0) == 5000.0
        assert self.employee.projected_salary(1) == 5250.0


import unittest

class TestEmployeeUnittest(unittest.TestCase):

    def setUp(self):
        self.employee = Employee("Jane", 30, 5000)

    def tearDown(self):
        del self.employee

    def test_employee_creation(self):
        assert self.employee.name == "Jane"

    def test_employee_projected_salary(self):
        assert self.employee.projected_salary(0) == 5000.0
        assert self.employee.projected_salary(1) == 5250.0

if __name__ == '__main__':
    unittest.main()



        
