# 06: Class-Based Decorators
print("Class-Based Decorators")
print("---------------------")

import functools
import time

# First, let's recall the structure of a function-based decorator
def function_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

# Now, here's the same decorator implemented as a class
class ClassTimer:
    def __init__(self, func):
        functools.update_wrapper(self, func)  # Preserve metadata
        self.func = func
    
    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        end = time.time()
        print(f"{self.func.__name__} took {end - start:.6f} seconds")
        return result

# Let's test both
@function_timer
def slow_function():
    time.sleep(0.1)
    return "Done"

@ClassTimer
def another_slow_function():
    time.sleep(0.1)
    return "Done too"

print("Comparing function and class decorators:")
slow_function()
another_slow_function()

# The real power of class decorators is maintaining state
class CallCounter:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0  # State maintained between calls
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CallCounter
def hello(name):
    return f"Hello, {name}!"

print("\nStateful decorator example:")
print(hello("Alice"))
print(hello("Bob"))
print(hello("Charlie"))

# Class decorators with parameters
class Repeat:
    def __init__(self, times=2):
        self.times = times
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(self.times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper

@Repeat(times=3)
def random_number():
    import random
    return random.randint(1, 10)

print("\nClass decorator with parameters:")
results = random_number()
print(f"Random numbers: {results}")

# A more complex example: rate limiting with class
class RateLimit:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Clean up old calls
            self.calls = [call for call in self.calls if call > now - self.period]
            
            # Check rate limit
            if len(self.calls) >= self.max_calls:
                wait_time = self.period - (now - self.calls[0])
                print(f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.")
                return None
            
            # Add this call and proceed
            self.calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper

@RateLimit(max_calls=3, period=5)
def api_call(endpoint):
    return f"Data from {endpoint}"

print("\nClass-based rate limiting:")
for i in range(5):
    result = api_call(f"/api/endpoint/{i}")
    if result:
        print(result)
    time.sleep(0.5)  # Brief delay between calls

# Class decorator with multiple methods
class ValidationDecorator:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
    
    def __call__(self, *args, **kwargs):
        # Pre-validation
        if not self.validate_args(*args, **kwargs):
            raise ValueError("Invalid arguments")
        
        # Call the function
        result = self.func(*args, **kwargs)
        
        # Post-validation
        if not self.validate_result(result):
            raise ValueError("Invalid result")
        
        return result
    
    def validate_args(self, *args, **kwargs):
        # In a real validator, we'd have actual logic here
        print(f"Validating args: {args}, kwargs: {kwargs}")
        return True
    
    def validate_result(self, result):
        # In a real validator, we'd have actual logic here
        print(f"Validating result: {result}")
        return True

@ValidationDecorator
def divide(a, b):
    return a / b

print("\nComplex class decorator with multiple methods:")
try:
    result = divide(10, 2)
    print(f"Result: {result}")
except ValueError as e:
    print(f"Error: {e}")

# Class decorator with inheritance
class BaseDecorator:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
    
    def __call__(self, *args, **kwargs):
        # Base functionality
        self.before()
        result = self.func(*args, **kwargs)
        self.after()
        return result
    
    def before(self):
        pass  # To be overridden
    
    def after(self):
        pass  # To be overridden

class LoggingDecorator(BaseDecorator):
    def before(self):
        print(f"Calling {self.func.__name__}")
    
    def after(self):
        print(f"Finished {self.func.__name__}")

@LoggingDecorator
def compute():
    print("Computing...")
    return 42

print("\nInherited class decorator:")
result = compute()
print(f"Computed: {result}")

