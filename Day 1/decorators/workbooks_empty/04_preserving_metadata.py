# 04: Preserving Metadata
print("Preserving Function Metadata in Decorators")
print("-----------------------------------------")

# First, let's see the problem
# TODO

@simple_decorator
def hello(name):
    """Return a personalized greeting message."""
    return f"Hello, {name}!"

print("Problem: Metadata is lost")
print(f"Function name: {hello.__name__}")  # Shows 'wrapper', not 'hello'
print(f"Docstring: {hello.__doc__}")       # Shows wrapper's docstring, not original
print(f"Argument count: {hello.__code__.co_argcount}")  # May not match original

# Let's fix this with functools.wraps
import functools

# TODO

@better_decorator
def greet(name):
    """Return a personalized greeting message."""
    return f"Hello, {name}!"

print("\nSolution: Using functools.wraps")
print(f"Function name: {greet.__name__}")  # Shows 'greet'
print(f"Docstring: {greet.__doc__}")       # Shows original docstring
print(f"Argument count: {greet.__code__.co_argcount}")  # Shows original count

# Let's see how this affects help() and introspection
print("\nComparing help() output:")
print("\n-- Without functools.wraps --")
help(hello)

print("\n-- With functools.wraps --")
help(greet)


# Showing the update_wrapper function
print("\nManually using update_wrapper:")

# TODO

@manual_decorator
def farewell(name):
    """Say goodbye to someone."""
    return f"Goodbye, {name}!"

print(f"Function name: {farewell.__name__}")  # Shows 'farewell'
print(f"Docstring: {farewell.__doc__}")       # Shows original docstring

# Inspect signature
import inspect

def decorator_with_different_signature(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # Different signature from original
        return func(*args, **kwargs)
    return wrapper

@decorator_with_different_signature
def add(a, b, c=0):
    """Add two or three numbers."""
    return a + b + c

print("\nInspecting function signature:")
print(f"Original signature: {inspect.signature(add)}")  # Shows (a, b, c=0)
print(f"Actual arguments needed: Still (a, b, c=0) as wraps preserves the signature")

# Real-world example with timing decorator
def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds to run")
        return result
    return wrapper

@timeit
def compute_primes(limit):
    """Compute prime numbers up to the given limit."""
    primes = []
    for num in range(2, limit + 1):
        for prime in primes:
            if num % prime == 0:
                break
        else:
            primes.append(num)
    return primes

print("\nUsing a well-formed timing decorator:")
primes = compute_primes(1000)
print(f"Found {len(primes)} prime numbers")
print(f"Function name: {compute_primes.__name__}")  # Shows 'compute_primes'
print(f"Docstring: {compute_primes.__doc__}")       # Shows original docstring

"""--- Exercise ---
1. Create a decorator that logs function calls to a file, including arguments and return values.
   Make sure to preserve function metadata.
2. Modify an existing decorator to preserve metadata, and explain the changes you made."""
