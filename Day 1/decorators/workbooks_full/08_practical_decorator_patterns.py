
# 08: Practical Decorator Patterns
print("Practical Decorator Patterns and Use Cases")
print("----------------------------------------")

import functools
import time
import random
import json
import requests
from datetime import datetime, timedelta

# Pattern 1: Memoization / Caching
print("Pattern 1: Memoization / Caching")
print("------------------------------")

def memoize(func):
    """Cache the results of a function call based on its arguments."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from the function arguments
        # For this simple example, we only use args
        if args in cache:
            print(f"Cache hit for {func.__name__}{args}")
            return cache[args]
        
        result = func(*args, **kwargs)
        cache[args] = result
        print(f"Cache miss for {func.__name__}{args}, stored result")
        return result
    
    return wrapper

@memoize
def fibonacci(n):
    """A classic example where memoization helps greatly."""
    print(f"Computing fibonacci({n})...")
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print("\nFibonacci with memoization:")
print(f"fibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(10) again = {fibonacci(10)}  # Should be cached")
print(f"fibonacci(8) = {fibonacci(8)}  # Should be cached from previous calculation")
print(f"fibonacci(12) = {fibonacci(12)}  # Partially cached")

# Pattern 2: Retry Logic
print("\nPattern 2: Retry Logic")
print("--------------------")

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Retry a function call on specified exceptions with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise  # Re-raise the last exception if all attempts failed
                    
                    print(f"Attempt {attempts} failed with {type(e).__name__}: {e}")
                    print(f"Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff  # Exponential backoff
            
            return None  # Should never reach here
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, backoff=2, exceptions=(ValueError, KeyError))
def unstable_operation():
    """A function that sometimes fails."""
    val = random.random()
    print(f"Running unstable operation (val={val:.2f})...")
    
    if val < 0.6:  # 60% chance of failure
        error_type = random.choice([ValueError, KeyError, TypeError])
        if error_type == ValueError:
            raise ValueError("Something went wrong!")
        elif error_type == KeyError:
            raise KeyError("Missing key!")
        else:
            raise TypeError("Wrong type!")  # This won't be retried
    
    return "Operation successful!"

print("\nRetry logic example:")
try:
    result = unstable_operation()
    print(f"Final result: {result}")
except Exception as e:
    print(f"Failed after retries: {type(e).__name__}: {e}")

# Pattern 3: Input/Output Validation
print("\nPattern 3: Input/Output Validation")
print("--------------------------------")

def validate(input_validator=None, output_validator=None):
    """Validate function inputs and outputs."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Validate inputs
            if input_validator:
                if not input_validator(*args, **kwargs):
                    raise ValueError(f"Invalid inputs to {func.__name__}: {args}, {kwargs}")
            
            # Call the function
            result = func(*args, **kwargs)
            
            # Validate output
            if output_validator and not output_validator(result):
                raise ValueError(f"Invalid output from {func.__name__}: {result}")
            
            return result
        return wrapper
    return decorator

# Input validator: check if all arguments are positive
def all_positive(*args, **kwargs):
    return all(arg > 0 for arg in args if isinstance(arg, (int, float)))

# Output validator: check if result is a positive number
def is_positive(result):
    return isinstance(result, (int, float)) and result > 0

@validate(input_validator=all_positive, output_validator=is_positive)
def calculate_rectangle_area(width, height):
    """Calculate the area of a rectangle."""
    return width * height

print("\nValidation decorator example:")
try:
    area = calculate_rectangle_area(5, 10)
    print(f"Rectangle area: {area}")
    
    # This should fail input validation
    area = calculate_rectangle_area(-5, 10)
    print("This won't execute")
except ValueError as e:
    print(f"Error: {e}")

# Pattern 4: Authentication and Authorization
print("\nPattern 4: Authentication and Authorization")
print("----------------------------------------")

# Mock user database and session system
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}

current_user = None

def login(username, password):
    """Mock login function."""
    global current_user
    if username in USERS and USERS[username]["password"] == password:
        current_user = {"username": username, "role": USERS[username]["role"]}
        return True
    return False

def logout():
    """Mock logout function."""
    global current_user
    current_user = None

def login_required(func):
    """Decorator that requires a user to be logged in."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if current_user is None:
            raise PermissionError("You must be logged in to access this function")
        return func(*args, **kwargs)
    return wrapper

def role_required(role):
    """Decorator that requires a specific role."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_user is None or current_user["role"] != role:
                raise PermissionError(f"You need the '{role}' role to access this function")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@login_required
def view_content():
    """Any logged-in user can view content."""
    return "Here's some content for logged-in users."

@login_required
@role_required("admin")
def admin_action():
    """Only admins can perform this action."""
    return "Performing admin action..."

print("\nAuthentication example:")
try:
    # Try without logging in
    content = view_content()
except PermissionError as e:
    print(f"Error: {e}")

# Log in as regular user
login("user", "user123")
print(f"Logged in as: {current_user['username']}")

try:
    # Regular user can view content
    content = view_content()
    print(f"Content: {content}")
    
    # But can't perform admin actions
    admin_content = admin_action()
    print(f"Admin action: {admin_content}")
except PermissionError as e:
    print(f"Error: {e}")

# Log in as admin
logout()
login("admin", "admin123")
print(f"Logged in as: {current_user['username']}")

try:
    # Admin can do both
    content = view_content()
    print(f"Content: {content}")
    
    admin_content = admin_action()
    print(f"Admin action: {admin_content}")
except PermissionError as e:
    print(f"Error: {e}")

# Pattern 5: Framework-Style Decorators (like Flask)
print("\nPattern 5: Framework-Style Decorators")
print("----------------------------------")

class MiniWebFramework:
    """A minimal web framework to demonstrate decorator usage."""
    
    def __init__(self):
        self.routes = {}
    
    def route(self, path):
        """Register a function as a route handler."""
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def handle_request(self, path, *args, **kwargs):
        """Simulate handling a request."""
        if path in self.routes:
            handler = self.routes[path]
            return handler(*args, **kwargs)
        return f"404 Not Found: {path}"

# Create a mini app
app = MiniWebFramework()

# Define routes using decorators
@app.route("/")
def index():
    return "Welcome to the home page!"

@app.route("/about")
def about():
    return "About our company..."

@app.route("/user")
def user_profile(user_id=None):
    if user_id:
        return f"Profile for user {user_id}"
    return "Please specify a user ID"

# Simulate requests
print("\nWeb framework example:")
print(f"GET /: {app.handle_request('/')}")
print(f"GET /about: {app.handle_request('/about')}")
print(f"GET /user?user_id=123: {app.handle_request('/user', user_id=123)}")
print(f"GET /nonexistent: {app.handle_request('/nonexistent')}")

# Pattern 6: Deprecation Warnings
print("\nPattern 6: Deprecation Warnings")
print("-----------------------------")

def deprecated(since=None, use_instead=None):
    """Mark a function as deprecated."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warning = f"Warning: {func.__name__} is deprecated"
            if since:
                warning += f" since version {since}"
            if use_instead:
                warning += f". Use {use_instead} instead"
            print(warning)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@deprecated(since="2.0", use_instead="new_function()")
def old_function():
    """This function is outdated."""
    return "Using the old implementation..."

print("\nDeprecation example:")
result = old_function()
print(f"Result: {result}")
