# 07: Method and Class Decorators
print("Decorating Methods and Classes")
print("-----------------------------")

import functools
import time

# Basic decorator as a reference
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

# Part 1: Decorating Instance Methods
print("Part 1: Decorating Instance Methods")
print("----------------------------------")

class MathOperations:
    def __init__(self, value):
        self.value = value
    
    @timer  # Decorating an instance method
    def factorial(self):
        """Calculate factorial of self.value"""
        if self.value == 0 or self.value == 1:
            return 1
        result = 1
        for i in range(2, self.value + 1):
            result *= i
        return result
    
    def square(self):
        return self.value ** 2

# Create an instance and call the decorated method
math = MathOperations(10)
print(f"Factorial of {math.value}: {math.factorial()}")


# Part 2: Working with Different Method Types
print("\nPart 2: Working with Method Types")
print("-------------------------------")

class Calculator:
    value = 100  # Class attribute
    
    def __init__(self, x):
        self.x = x
    
    @timer
    def compute(self):
        """Instance method - has access to self"""
        time.sleep(0.1)
        return self.x * 2
    
    @classmethod
    @timer  # Stacking built-in and custom decorators
    def class_compute(cls):
        """Class method - has access to cls"""
        time.sleep(0.1)
        return cls.value * 2
    
    @staticmethod
    @timer  # Notice the order of decorators
    def static_compute(x):
        """Static method - no access to instance or class"""
        time.sleep(0.1)
        return x * 2
    
    # Using the built-in property decorator
    @property
    def double_x(self):
        """Property method - accessed like an attribute"""
        return self.x * 2

calc = Calculator(5)
print(f"Instance method: {calc.compute()}")
print(f"Class method: {Calculator.class_compute()}")
print(f"Static method: {Calculator.static_compute(10)}")
print(f"Property: {calc.double_x}")  # Notice: no parentheses

# Part 3: Creating Custom Method Decorators
print("\nPart 3: Custom Method Decorators")
print("------------------------------")

def require_positive(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check if the instance has positive value
        if self.value <= 0:
            raise ValueError("Value must be positive")
        return func(self, *args, **kwargs)
    return wrapper

class Values:
    def __init__(self, value):
        self.value = value
    
    @require_positive
    def reciprocal(self):
        return 1 / self.value

# Test with valid and invalid values
try:
    v1 = Values(5)
    print(f"Reciprocal: {v1.reciprocal()}")
    
    v2 = Values(-5)
    print(f"This won't execute: {v2.reciprocal()}")
except ValueError as e:
    print(f"Error: {e}")

# Part 4: Decorating Classes
print("\nPart 4: Decorating Entire Classes")
print("-------------------------------")

# A simple class decorator
def add_greeting(cls):
    # Add a new method to the class
    def say_hello(self):
        return f"Hello from {self.__class__.__name__} with {self.name}!"
    
    # Add the new method to the class
    cls.say_hello = say_hello
    
    # Return the modified class
    return cls

@add_greeting
class Person:
    def __init__(self, name):
        self.name = name

# Create an instance and use the added method
person = Person("Alice")
print(person.say_hello())  # Output: Hello from Person with Alice!

# Decorator for creating singleton classes
def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    # Keep track of the unique instance
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        print(f"Connecting to {host}:{port}...")
    
    def query(self, sql):
        return f"Executing {sql} on {self.host}"

# Create "two" instances - should only create one
print("\nSingleton example:")
db1 = DatabaseConnection("localhost", 5432)
db2 = DatabaseConnection("example.com", 8000)  # Should reuse db1

print(f"Same instance? {db1 is db2}")  # True
print(f"Host of db2: {db2.host}")  # localhost, not example.com


# Creating a validator for class attributes
def validate_attributes(**validators):
    def decorator(cls):
        # Store the original __init__
        original_init = cls.__init__
        
        # Create a new __init__ that validates attributes
        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            # Call the original __init__
            original_init(self, *args, **kwargs)
            
            # Validate each attribute with its validator
            for attr_name, validator in validators.items():
                if hasattr(self, attr_name):
                    value = getattr(self, attr_name)
                    if not validator(value):
                        raise ValueError(f"Invalid value for {attr_name}: {value}")
        
        # Replace __init__ with our new version
        cls.__init__ = new_init
        return cls
    
    return decorator

# Using the validator
@validate_attributes(
    age=lambda x: isinstance(x, int) and x >= 0,
    email=lambda x: isinstance(x, str) and '@' in x
)
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

print("\nAttribute validation example:")
try:
    user1 = User("Bob", 30, "bob@example.com")
    print(f"Valid user: {user1.name}, {user1.age}, {user1.email}")
    
    user2 = User("Alice", -5, "alice@example.com")
    print("This won't execute")
except ValueError as e:
    print(f"Error: {e}")
