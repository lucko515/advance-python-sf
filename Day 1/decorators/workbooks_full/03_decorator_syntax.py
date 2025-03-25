
# 03: Decorator Syntax
print("Python Decorator Syntax (@)")
print("---------------------------")

# Let's create some simple decorators to use
def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

def underline(func):
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper

# Manual approach (from previous lesson)
print("Manual decorator application:")

def greeting(name):
    return f"Hello, {name}!"

# This is how we manually apply decorators
decorated_greeting = bold(italic(greeting))
print(decorated_greeting("Alice"))  # <b><i>Hello, Alice!</i></b>

# Now let's use decorator syntax
print("\nUsing @ decorator syntax:")

@bold
@italic
def greeting_decorated(name):
    return f"Hello, {name}!"

print(greeting_decorated("Bob"))  # <b><i>Hello, Bob!</i></b>

print("\nThis is equivalent to:")
print("greeting_decorated = bold(italic(greeting_decorated))")

# The order of decorators matters
print("\nOrder matters:")

@italic
@bold
def greeting_reversed(name):
    return f"Hello, {name}!"

print(greeting_reversed("Charlie"))  # <i><b>Hello, Charlie!</b></i>

# Stacking more decorators
print("\nStacking multiple decorators:")

@underline
@bold
@italic
def triple_decorated(name):
    return f"Hello, {name}!"

print(triple_decorated("Dave"))  # <u><b><i>Hello, Dave!</i></b></u>


# Decorators are applied at function definition time
print("\nDecorators are applied at function definition time:")

def debug_decorator(func):
    print(f"Applying decorator to {func.__name__}")
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

print("About to define the function...")

@debug_decorator
def add(a, b):
    return a + b

print("Function defined. Now calling it...")
result = add(3, 5)
print(f"Final result: {result}")

# Using a decorator with arguments
print("\nUsing a decorator that takes parameters:")

"""
Exercise:
1. Create a decorator that prints a line of dashes before and after the function output.
2. Create two decorators: one that converts the output to uppercase and one that adds
   an exclamation mark at the end. Apply both to a function and observe the results.
"""
