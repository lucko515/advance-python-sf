# 01: Python Object Model Fundamentals
print("Python Object Model Fundamentals")
print("-------------------------------")

# Everything in Python is an object
print("1. Everything in Python is an object")
print(f"Type of 42: {type(42)}")
print(f"Type of 'hello': {type('hello')}")
print(f"Type of [1, 2, 3]: {type([1, 2, 3])}")

def example_function():
    pass

print(f"Type of a function: {type(example_function)}")

class ExampleClass:
    pass

print(f"Type of a class: {type(ExampleClass)}")
print(f"Type of a class instance: {type(ExampleClass())}")
print(f"Type of type itself: {type(type)}")

print("\n2. Objects have attributes and methods")
example_list = [1, 2, 3]
print(f"List methods: append, extend, insert, ...")
print(f"List has {len(dir(example_list))} attributes/methods")

# The __dict__ attribute - where instance attributes are stored
print("\n3. The __dict__ attribute")
class Person:
    species = "Homo sapiens"  # class attribute
    
    def __init__(self, name, age):
        self.name = name      # instance attribute
        self.age = age        # instance attribute
    
    def greet(self):
        return f"Hello, my name is {self.name}"

alice = Person("Alice", 30)
bob = Person("Bob", 25)

print(f"Alice's __dict__: {alice.__dict__}")
print(f"Bob's __dict__: {bob.__dict__}")
print(f"Person class __dict__ keys: {list(Person.__dict__.keys())[:5]} ...")

# Modifying attributes
print("\n4. Dynamic attribute modification")
alice.job = "Developer"
print(f"Alice's __dict__ after adding job: {alice.__dict__}")

# Understanding class vs instance attributes
print("\n5. Class vs Instance attributes")
print(f"Alice's species: {alice.species}")
print(f"Bob's species: {bob.species}")
print(f"Person.species: {Person.species}")

# Change the class attribute
Person.species = "Homo digitalis"
print(f"After changing Person.species:")
print(f"Alice's species: {alice.species}")
print(f"Bob's species: {bob.species}")

# Override with instance attribute
alice.species = "Individual species"
print(f"After setting alice.species:")
print(f"Alice's species: {alice.species}")
print(f"Bob's species: {bob.species}")

# Method Resolution Order (MRO)
print("\n6. Method Resolution Order (MRO)")
class A:
    def method(self):
        return "A.method"

class B(A):
    def method(self):
        return "B.method"

class C(A):
    def method(self):
        return "C.method"

class D(B, C):
    pass

print(f"D's MRO: {[cls.__name__ for cls in D.__mro__]}")
d = D()
print(f"d.method() returns: {d.method()}")  # Will use B's method due to MRO

# Special methods
print("\n7. Special methods")
class Number:
    def __init__(self, value):
        self.value = value
    
    def __add__(self, other):
        return Number(self.value + other.value)
    
    def __str__(self):
        return f"Number({self.value})"
    
    def __eq__(self, other):
        return self.value == other.value

n1 = Number(5)
n2 = Number(10)
print(f"n1: {n1}")
print(f"n1 + n2: {n1 + n2}")
print(f"n1 == Number(5): {n1 == Number(5)}")

# Object creation process
print("\n8. Object creation process")
class CustomObject:
    def __new__(cls, *args, **kwargs):
        print(f"1. __new__ called: creating instance of {cls.__name__}")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, name):
        print(f"2. __init__ called: initializing with name={name}")
        self.name = name

obj = CustomObject("Test")
print(f"Object created: {obj.name}")

"""--- Exercise ---
1. Create a class with a custom __getattribute__ method that logs all attribute access."""
