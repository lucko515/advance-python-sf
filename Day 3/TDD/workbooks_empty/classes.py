class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."


class Employee(Person):
    def __init__(self, name, age, salary):
        super().__init__(name, age)
        self.salary = salary

    def get_salary(self):
        return self.salary

    def projected_salary(self, years):
        return self.salary * (1 + 0.05) ** years





