# 01: Functions as Objects
print("Python Functions as First-Class Objects")
print("---------------------------------------")

# Functions in Python are objects that can be assigned to variables
# TODO

# We can assign a function to a variable
greeting_function = greet

# And use that variable to call the function
print("Function assigned to variable:")
print(greeting_function("Alice"))  # Output: Hello, Alice!

# Functions have types and attributes like other objects
print("\nFunction type:", type(greet))
print("Function attributes:", dir(greet)[:5], "...")  # Show first 5 attributes

# Functions can be stored in data structures
function_list = [greet, str.upper, len]
print("\nCalling functions from a list:")
print(function_list[0]("Bob"))    # Output: Hello, Bob!
print(function_list[1]("bob"))    # Output: BOB
print(function_list[2]("bob"))    # Output: 3

# Functions can be passed as arguments to other functions
# TODO

print("\nPassing functions as arguments:")
print(execute_function(greet, "Charlie"))  # Output: Hello, Charlie!
print(execute_function(len, "Charlie"))    # Output: 7

# Higher-order functions: functions that return other functions
def create_multiplier(factor):
    return None

# Create specific multiplier functions
double = create_multiplier(2)
triple = create_multiplier(3)

print("\nFunctions returning functions:")
print(f"Double 5: {double(5)}")  # Output: 10
print(f"Triple 5: {triple(5)}")  # Output: 15

"""
Exercise:
1. Create a function that takes another function and a list as arguments,
   and applies the function to each element of the list.
2. Create a function that returns a greeting function for a specific language.
   For example, get_greeting_function('Spanish') would return a function that greets in Spanish.
"""