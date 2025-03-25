
# 05: Decorators with Arguments
print("Creating Decorators with Arguments")
print("--------------------------------")

import functools
import time

# First, let's recall a basic decorator without arguments
def simple_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds to run")
        return result
    return wrapper

@simple_timer
def calculate_sum(n):
    return sum(range(n))

print("Basic decorator without arguments:")
result = calculate_sum(1000000)
print(f"Sum: {result}")

# Now, let's create a decorator that accepts arguments
# TODO:

@timer_with_message("Execution time")
def calculate_product(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print("\nDecorator with a single argument:")
result = calculate_product(10)
print(f"Product: {result}")

# Decorator with multiple arguments
# TODO
def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        results = []
        for i in range(times):
            if message:
                print(f"{message} - iteration {i+1}/{times}")
            results.append(func(*args, **kwargs))
        return results
    return wrapper

@repeat(times=3, message="Repeating calculation")
def roll_dice():
    import random
    return random.randint(1, 6)

print("\nDecorator with multiple arguments:")
results = roll_dice()
print(f"Dice rolls: {results}")

# Decorator with optional arguments
def debug(func=None, *, prefix=''):
    # This pattern allows the decorator to be used with or without arguments
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            print(f"{prefix}Calling {func.__name__}({signature})")
            result = func(*args, **kwargs)
            print(f"{prefix}{func.__name__} returned {result!r}")
            return result
        return wrapper
    
    # This allows the decorator to work with or without arguments
    if func is None:
        # Called with arguments: @debug(prefix='>>>')
        return decorator
    else:
        # Called without arguments: @debug
        return decorator(func)

# Used without arguments
@debug
def greet(name):
    return f"Hello, {name}!"

# Used with arguments
@debug(prefix='>>> ')
def add(a, b):
    return a + b

print("\nDecorator with optional arguments:")
greet("Alice")
add(5, 3)

# Real-world example: rate limiting decorator
def rate_limit(max_calls, period):
    """Limit the number of calls to a function within a time period."""
    def decorator(func):
        calls = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove calls older than the period
            while calls and calls[0] < now - period:
                calls.pop(0)
                
            # Check if we've hit the rate limit
            if len(calls) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {period} seconds")
                
            calls.append(now)
            return func(*args, **kwargs)
            
        return wrapper
    return decorator

@rate_limit(max_calls=3, period=1)
def api_request(endpoint):
    print(f"Requesting data from {endpoint}")
    return {"data": "sample response"}

print("\nRate limiting decorator example:")
try:
    for i in range(5):
        api_request(f"/api/endpoint/{i}")
except Exception as e:
    print(f"Exception caught: {e}")