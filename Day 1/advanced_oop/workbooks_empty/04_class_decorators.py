# 04: Class Decorators
print("Class Decorators")
print("---------------")

# Brief review of function decorators
print("1. Function Decorators Review")
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to run")
        return result
    return wrapper

@timing_decorator
def slow_function():
    import time
    time.sleep(0.1)
    return "Function completed"

print(slow_function())

# Basic class decorator
print("\n2. Basic Class Decorator")
def add_repr(cls):
    """Class decorator that adds a __repr__ method to the class."""
    def __repr__(self):
        attrs = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    
    # Add the __repr__ method to the class
    cls.__repr__ = __repr__
    
    # Return the modified class
    return cls

@add_repr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(f"Person with auto-generated __repr__: {person}")

# Class decorator with arguments
print("\n3. Class Decorator with Arguments")
def validate_attributes(*required_attrs):
    """Class decorator that validates required attributes at initialization."""
    def decorator(cls):
        # Store the original __init__
        original_init = cls.__init__
        
        # Define a new __init__ that validates attributes
        def __init__(self, *args, **kwargs):
            # Call the original __init__
            original_init(self, *args, **kwargs)
            
            # Check for required attributes
            missing_attrs = [attr for attr in required_attrs 
                            if not hasattr(self, attr) or getattr(self, attr) is None]
            if missing_attrs:
                raise ValueError(f"Missing required attributes: {', '.join(missing_attrs)}")
        
        # Replace the __init__ method
        cls.__init__ = __init__
        
        return cls
    
    return decorator

@validate_attributes('name', 'email')
class User:
    def __init__(self, name=None, email=None, age=None):
        self.name = name
        self.email = email
        self.age = age

try:
    valid_user = User("Bob", "bob@example.com")
    print(f"Created valid user: {valid_user.name}")
    
    invalid_user = User("Charlie")  # Missing email
    print(f"Created invalid user: {invalid_user.name}")
except ValueError as e:
    print(f"Error creating user: {e}")

# Implementing the Singleton pattern with a class decorator
print("\n4. Singleton Pattern with Class Decorator")
def singleton(cls):
    """Class decorator that implements the Singleton pattern."""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    # Replace the class with the get_instance function
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self, db_name):
        print(f"Initializing database connection to {db_name}")
        self.db_name = db_name
    
    def query(self, sql):
        return f"Executing query on {self.db_name}: {sql}"

# Should only initialize once
db1 = DatabaseConnection("users_db")
db2 = DatabaseConnection("products_db")  # Should not re-initialize

print(f"db1.db_name: {db1.db_name}")
print(f"db2.db_name: {db2.db_name}")  # Will still be "users_db"
print(f"db1 is db2: {db1 is db2}")

# Decorator for automatic registration
print("\n5. Registry Pattern with Class Decorator")
def register(registry):
    """Class decorator that registers classes in a registry."""
    def decorator(cls):
        name = getattr(cls, 'name', cls.__name__)
        registry[name] = cls
        return cls
    return decorator

# Global registry
handlers = {}

@register(handlers)
class JSONHandler:
    name = "json"
    
    def process(self, data):
        return f"Processing {data} as JSON"

@register(handlers)
class XMLHandler:
    name = "xml"
    
    def process(self, data):
        return f"Processing {data} as XML"

print(f"Registered handlers: {list(handlers.keys())}")
print(f"Using JSON handler: {handlers['json']().process('data')}")

# Combining multiple class decorators
print("\n6. Combining Multiple Class Decorators")
def log_methods(cls):
    """Class decorator that adds logging to all methods."""
    for name, method in cls.__dict__.items():
        # Only process callable attributes that don't start with __
        if callable(method) and not name.startswith('__'):
            setattr(cls, name, log_method_calls(method))
    return cls

def log_method_calls(method):
    """Decorator for individual methods."""
    def wrapper(self, *args, **kwargs):
        print(f"Calling {method.__name__} with args={args}, kwargs={kwargs}")
        result = method(self, *args, **kwargs)
        print(f"Method {method.__name__} returned {result}")
        return result
    return wrapper

@add_repr
@log_methods
@validate_attributes('name')
class Service:
    def __init__(self, name, port=8080):
        self.name = name
        self.port = port
    
    def start(self):
        return f"Starting {self.name} on port {self.port}"
    
    def stop(self):
        return f"Stopping {self.name}"

service = Service("web_server", 80)
service.start()
service.stop()

# Class decorators vs. metaclasses
print("\n7. Class Decorators vs. Metaclasses")

# Real-world example: creating a simple API framework
print("\n8. Real-world Example: Simple API Framework")
def api_controller(prefix=""):
    """Class decorator that registers API endpoints defined in the class."""
    def decorator(cls):
        # Create an empty endpoints registry if it doesn't exist
        if not hasattr(cls, 'endpoints'):
            cls.endpoints = {}
        
        # Scan for methods decorated with @endpoint
        for name, method in cls.__dict__.items():
            if hasattr(method, 'is_endpoint') and method.is_endpoint:
                # Register the endpoint with its path
                path = f"{prefix}{method.path}"
                cls.endpoints[path] = method
        
        # Add a method to get all endpoints
        def get_endpoints(self):
            return {path: getattr(self, method.__name__) 
                    for path, method in self.__class__.endpoints.items()}
        
        cls.get_endpoints = get_endpoints
        
        return cls
    
    return decorator

# Method decorator to mark a method as an API endpoint
def endpoint(path):
    """Method decorator that marks a method as an API endpoint."""
    def decorator(method):
        method.is_endpoint = True
        method.path = path
        return method
    return decorator

# Usage example
@api_controller(prefix="/api")
class UserController:
    def __init__(self):
        self.users = {}
    
    @endpoint("/users")
    def get_users(self, request=None):
        return {"users": list(self.users.values())}
    
    @endpoint("/users/{id}")
    def get_user(self, user_id, request=None):
        return {"user": self.users.get(user_id)}
    
    def internal_method(self):
        """This method won't be registered as an endpoint."""
        return "Internal logic"

# Create a controller and inspect its endpoints
controller = UserController()
print(f"API endpoints: {list(controller.endpoints.keys())}")

for path, method in controller.get_endpoints().items():
    print(f"Endpoint {path} -> {method.__name__}")
