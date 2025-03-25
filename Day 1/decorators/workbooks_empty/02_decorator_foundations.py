
import time

# 02: Decorator Foundations
print("Understanding Decorator Foundations")
print("---------------------------------")

# A simple function we want to enhance
def greet(name):
    return f"Hello, {name}!"

print("Original function:")
print(greet("Alice"))  # Output: Hello, Alice!

# A function that will act as a decorator
# TODO: announce function

# Manually decorating our function
enhanced_greet = announce(greet)

print("\nCalling the enhanced function:")
result = enhanced_greet("Bob")
print(f"Result: {result}")


# Another example: Timing how long a function takes to execute
# TODO measure_time

# A function that does some work
def compute_squares(n):
    print(f"Computing squares of numbers 1 to {n}...")
    result = [i**2 for i in range(1, n+1)]
    return result

# Apply our timing decorator
timed_compute = measure_time(compute_squares)

print("\nTiming a function:")
result = timed_compute(1000)
print(f"Computed {len(result)} squares")

# Example with multiple decorators
# TODO logged_and_timed_compute

# Applying multiple decorators (manually, still without @ syntax)
print("\nMultiple decorators:")
logged_and_timed_compute = log_function_call(measure_time(compute_squares))
result = logged_and_timed_compute(100)


"""
Exercise:
1. Create a decorator function that counts how many times a function is called.
2. Create a decorator that caches the results of a function for repeated calls with the same arguments.
"""
