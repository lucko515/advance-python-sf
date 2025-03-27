import pytest
from classes import Person, Employee

class TestPerson:
    
    def setup_method(self):
        self.person = Person("John", 30)

    def teardown_method(self):
        del self.person

    def test_person_creation(self):
        assert self.person.name == "John"
        assert self.person.age == 30

class TestEmployee:

    def setup_method(self):
        self.employee = Employee("Jane", 25, 50000)

    def teardown_method(self):
        del self.employee

    @pytest.mark.skip(reason="This feature is not implemented yet")
    def test_employee_creation(self):
        assert self.employee.name == "Jane"
        assert self.employee.age == 25
        assert self.employee.salary == 50000

    def test_employee_salary(self):
        assert self.employee.get_salary() == 50000

    def test_employee_projected_salary(self):
        assert self.employee.projected_salary(1) == 52500
        assert self.employee.projected_salary(0) == 50000

    def test_employee_inheritance(self):
        assert self.employee.say_hello() == "Hello, my name is Jane and I am 25 years old."









        
