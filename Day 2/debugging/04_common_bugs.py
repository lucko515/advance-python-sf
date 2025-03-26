# 04: Common Python Bugs and How to Debug Them
print("Common Python Bugs and How to Debug Them")
print("--------------------------------------")

# 1. Syntax Errors
print("\n1. Syntax Errors")
print("--------------")
print("These prevent your code from running at all.")

# Example of a syntax error (commented out so this file can run)
"""
# Missing closing parenthesis
print("Hello, world!"
"""
# 2. Runtime Errors (Exceptions)
print("\n2. Runtime Errors (Exceptions)")
print("----------------------------")
print("These occur during program execution.")

# Example of common runtime errors
def demonstrate_runtime_errors():
    try:
        # IndexError
        my_list = [1, 2, 3]
        print(f"Trying to access index 10: {my_list[10]}")
    except IndexError as e:
        print(f"IndexError: {e}")
    
    try:
        # KeyError
        my_dict = {'a': 1, 'b': 2}
        print(f"Trying to access key 'c': {my_dict['c']}")
    except KeyError as e:
        print(f"KeyError: {e}")
    
    try:
        # TypeError
        print("Adding string and number: " + "hello" + 5)
    except TypeError as e:
        print(f"TypeError: {e}")
    
    try:
        # ZeroDivisionError
        print(f"Dividing by zero: {10 / 0}")
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError: {e}")
    
    try:
        # AttributeError
        number = 42
        print(f"Calling string method on number: {number.upper()}")
    except AttributeError as e:
        print(f"AttributeError: {e}")

demonstrate_runtime_errors()

# 3. Logical Errors
print("\n3. Logical Errors")
print("---------------")
print("These don't raise exceptions but produce incorrect results.")

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    # Logical error: forgot to divide by length
    return total  # Should be: return total / len(numbers)

numbers = [10, 20, 30, 40, 50]
avg = calculate_average(numbers)
print(f"Average of {numbers}: {avg}")
print(f"Expected result: {sum(numbers) / len(numbers)}")

def find_max(numbers):
    """Find the maximum value in a list."""
    if not numbers:
        return None
        
    # Logical error: initializing max_value incorrectly
    max_value = 0  # Should be: max_value = numbers[0]
    
    for num in numbers:
        if num > max_value:
            max_value = num
    
    return max_value

test_list = [-10, -20, -5, -30]
max_val = find_max(test_list)
print(f"Max value in {test_list}: {max_val}")
print(f"Expected result: {max(test_list)}")

# 4. Python-Specific Bugs
print("\n4. Python-Specific Bugs")
print("---------------------")
print("These are related to Python's unique behavior and design.")

# Mutable default arguments
print("\n4.1 Mutable Default Arguments")

def add_item(item, items=[]):  # Bug: mutable default
    items.append(item)
    return items

print(f"First call: {add_item('apple')}")
print(f"Second call: {add_item('orange')}")  # Unexpected: ['apple', 'orange']
print(f"Third call: {add_item('banana')}")   # Unexpected: ['apple', 'orange', 'banana']

print("\nCorrect version:")

def add_item_fixed(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(f"First call: {add_item_fixed('apple')}")
print(f"Second call: {add_item_fixed('orange')}")  # Correct: ['orange']

# Late binding closures
print("\n4.2 Late Binding Closures")

def create_multipliers():
    multipliers = []
    
    for i in range(1, 4):
        # Bug: i is evaluated when the function is called, not when it's defined
        def multiplier(x):
            return x * i
        multipliers.append(multiplier)
    
    return multipliers

multipliers = create_multipliers()
print(f"Multiplier 1(10): {multipliers[0](10)}")  # Unexpected: 30 (not 10)
print(f"Multiplier 2(10): {multipliers[1](10)}")  # Unexpected: 30 (not 20)
print(f"Multiplier 3(10): {multipliers[2](10)}")  # Expected: 30

print("\nCorrect version:")

def create_multipliers_fixed():
    multipliers = []
    
    for i in range(1, 4):
        # Capture i in a default argument, which is evaluated at function definition time
        def multiplier(x, i=i):
            return x * i
        multipliers.append(multiplier)
    
    return multipliers

multipliers_fixed = create_multipliers_fixed()
print(f"Multiplier 1(10): {multipliers_fixed[0](10)}")  # Correct: 10
print(f"Multiplier 2(10): {multipliers_fixed[1](10)}")  # Correct: 20
print(f"Multiplier 3(10): {multipliers_fixed[2](10)}")  # Correct: 30

# Name shadowing
print("\n4.3 Name Shadowing")

len = lambda x: "Oops, not the real len"  # Shadows the built-in len function
print(f"My list has length: {len([1, 2, 3])}")  # Unexpected result

# Restore the built-in len
del len
from builtins import len
print(f"My list has actual length: {len([1, 2, 3])}")  # Correct: 3

# 5. Debugging Strategies for Different Bug Types
print("\n5. Debugging Strategies for Different Bug Types")
print("--------------------------------------------")

# 6. Assertions and Defensive Programming
print("\n6. Assertions and Defensive Programming")
print("------------------------------------")

def divide_safely(a, b):
    """Safely divide two numbers."""
    # Defensive pre-condition checks
    assert isinstance(a, (int, float)), f"a must be a number, got {type(a)}"
    assert isinstance(b, (int, float)), f"b must be a number, got {type(b)}"
    assert b != 0, "Cannot divide by zero"
    
    result = a / b
    
    # Defensive post-condition check
    assert isinstance(result, float), f"Expected float result, got {type(result)}"
    return result

try:
    print(f"10 / 2 = {divide_safely(10, 2)}")
    print(f"10 / 0 = {divide_safely(10, 0)}")  # Will trigger assertion
except AssertionError as e:
    print(f"Assertion failed: {e}")