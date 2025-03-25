
# 09: Debugging and Testing Decorators
print("Debugging and Testing Code with Decorators")
print("----------------------------------------")

import functools
import time
import inspect
import unittest
from unittest import mock

# First, let's create a few decorators to work with
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg <= 0 for arg in args if isinstance(arg, (int, float))):
            raise ValueError("All arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

# Part 1: Debugging Challenges with Decorators
print("Part 1: Debugging Challenges")
print("--------------------------")

# Create some decorated functions
@log_calls
@timer
@validate_positive
def calculate_power(base, exponent):
    """Calculate base raised to the power of exponent."""
    return base ** exponent

# The problem: function looks different in stack traces
try:
    result = calculate_power(2, -3)
except ValueError as e:
    import traceback
    print("Error caught:")
    print(f"{type(e).__name__}: {e}")
    print("\nFirst few lines of traceback:")
    traceback.print_exc(limit=3)

# The decorator call chain can be confusing
print("\nDecorator call chain:")
print("1. calculate_power = log_calls(timer(validate_positive(calculate_power)))")
print("2. When you call calculate_power(2, -3):")
print("   a. First, log_calls's wrapper executes")
print("   b. It calls timer's wrapper")
print("   c. timer's wrapper calls validate_positive's wrapper")
print("   d. validate_positive's wrapper would call the original function, but raises an error")

# Part 2: Introspecting Decorated Functions
print("\nPart 2: Introspecting Decorated Functions")
print("-------------------------------------")

# Checking what our decorated function looks like
print(f"Function name: {calculate_power.__name__}")
print(f"Function docstring: {calculate_power.__doc__}")
print(f"Function module: {calculate_power.__module__}")

# Accessing the original function
print("\nAccessing the original function:")
if hasattr(calculate_power, "__wrapped__"):
    original_func = calculate_power.__wrapped__
    print(f"Original function through __wrapped__: {original_func.__name__}")
    
    # Is original_func the actual original? No, it's the next decorator in the chain
    if hasattr(original_func, "__wrapped__"):
        next_original = original_func.__wrapped__
        print(f"Next in chain: {next_original.__name__}")
        
        if hasattr(next_original, "__wrapped__"):
            final_original = next_original.__wrapped__
            print(f"Final original: {final_original.__name__}")

# Getting the full unwrapped function
def get_original_func(decorated_func):
    """Recursively unwrap a decorated function to find the original."""
    if hasattr(decorated_func, "__wrapped__"):
        return get_original_func(decorated_func.__wrapped__)
    return decorated_func

print("\nUnwrapping completely:")
original = get_original_func(calculate_power)
print(f"Completely unwrapped function: {original.__name__}")

# Part 3: Testing Functions with Decorators
print("\nPart 3: Testing Functions with Decorators")
print("-------------------------------------")

# Challenge: How do we test a function without triggering its decorators?
@log_calls
def expensive_operation(n):
    """An expensive operation we want to test efficiently."""
    result = 0
    for i in range(n):
        result += i
        time.sleep(0.001)  # Simulate work
    return result

print("\nProblem: Decorators interfere with testing")
print("- Decorators might log to console during tests")
print("- Decorators might add overhead to test runtime")
print("- Decorator behavior might hide function behavior")

# Solution 1: Access the original function through __wrapped__
print("\nSolution 1: Access __wrapped__ attribute")
if hasattr(expensive_operation, "__wrapped__"):
    unwrapped = expensive_operation.__wrapped__
    # Now we can test unwrapped directly
    result = unwrapped(10)
    print(f"Result calling unwrapped directly: {result}")

# Solution 2: Mock the decorator during tests
print("\nSolution 2: Mock the decorator")
print("In a test, you could do:")
print("with mock.patch('__main__.log_calls', lambda f: f):")
print("    # The decorator is bypassed in this context")
print("    result = expensive_operation(10)")

# Let's actually do it:
with mock.patch('__main__.log_calls', lambda f: f):
    # The decorator is bypassed in this context
    result = expensive_operation(10)
    print(f"Result with mocked decorator: {result}")

# Solution 3: Provide a test-only alternative
def add_numbers(a, b):
    """Regular function version."""
    return a + b

# For production
production_add = log_calls(add_numbers)

print("\nSolution 3: Separate decorated and undecorated versions")
print(f"Regular result: {add_numbers(5, 3)}")
print(f"Decorated result: {production_add(5, 3)}")

# Part 4: Testing Decorators Themselves
print("\nPart 4: Testing Decorators Themselves")
print("----------------------------------")

# Option 1: Test with a simple function
def test_func():
    """Simple function for testing decorators."""
    return "test result"

# Decorate the test function
decorated_test = timer(test_func)

print("\nTesting decorator with a simple function:")
result = decorated_test()
print(f"Result: {result}")

# Option 2: Create a test class
class TestTimer(unittest.TestCase):
    def test_timer_preserves_result(self):
        """Test that the timer decorator preserves the function result."""
        def func():
            return 42
            
        decorated = timer(func)
        self.assertEqual(decorated(), 42)
    
    def test_timer_preserves_metadata(self):
        """Test that the timer decorator preserves function metadata."""
        @timer
        def func():
            """Docstring."""
            pass
            
        self.assertEqual(func.__name__, "func")
        self.assertEqual(func.__doc__, "Docstring.")

# Part 5: Common Pitfalls and Best Practices
print("\nPart 5: Common Pitfalls and Best Practices")
print("---------------------------------------")

# Pitfall 1: Not preserving function metadata
def bad_decorator(func):
    def wrapper(*args, **kwargs):  # Missing functools.wraps!
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def function_with_metadata():
    """This function has a docstring."""
    pass

print("\nPitfall 1: Not preserving metadata")
print(f"Function name: {function_with_metadata.__name__}")  # Shows 'wrapper', not 'function_with_metadata'
print(f"Docstring: {function_with_metadata.__doc__}")       # None, not the original docstring

# Pitfall 2: Decorators that modify function signature
def add_parameter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Add a new parameter 'extra'
        kwargs['extra'] = 'added by decorator'
        return func(*args, **kwargs)
    return wrapper

@add_parameter
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

# This will raise TypeError because greet doesn't accept 'extra'
print("\nPitfall 2: Modifying function signature")
try:
    result = greet("Alice")
    print(f"Result: {result}")
except TypeError as e:
    print(f"Error: {e}")

# Pitfall 3: Decorators that aren't idempotent
def count_calls(func):
    count = 0
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Call #{count} to {func.__name__}")
        return func(*args, **kwargs)
    
    return wrapper

# What happens if we apply the same decorator twice?
@count_calls
@count_calls
def double_decorated():
    return "Result"

print("\nPitfall 3: Non-idempotent decorators")
result = double_decorated()
print(f"Result: {result}")
result = double_decorated()
print(f"Result: {result}")
