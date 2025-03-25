# 07: Custom Descriptors
print("Custom Descriptors")
print("----------------")

# Review of descriptor protocol
print("1. Review of Descriptor Protocol")
print("A descriptor is an object with any of these methods:")
print("- __get__(self, obj, type=None) -> value")
print("- __set__(self, obj, value) -> None")
print("- __delete__(self, obj) -> None")

# Common descriptor state storage patterns
print("\n2. Descriptor State Storage Patterns")

# Pattern 1: Using a dictionary in the descriptor
print("\nPattern 1: Dictionary in the descriptor")
class DictStorage:
    def __init__(self, initial_value=None):
        self.values = {}
        self.initial_value = initial_value
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Use id(obj) as key to the dictionary
        return self.values.get(id(obj), self.initial_value)
    
    def __set__(self, obj, value):
        self.values[id(obj)] = value
    
    def __delete__(self, obj):
        if id(obj) in self.values:
            del self.values[id(obj)]

# Pattern 2: Using instance __dict__
print("\nPattern 2: Using instance __dict__")
class DictAttrStorage:
    def __init__(self, name):
        self.name = name  # The attribute name
    
    def __set_name__(self, owner, name):
        # This method is called when the descriptor is assigned to a class
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Look up value in the instance __dict__
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        # Store value in the instance __dict__
        obj.__dict__[self.name] = value
    
    def __delete__(self, obj):
        if self.name in obj.__dict__:
            del obj.__dict__[self.name]

# Pattern 3: Using a naming convention
print("\nPattern 3: Using a naming convention")
class ConventionStorage:
    def __init__(self):
        self.name = None  # Will be set in __set_name__
    
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"  # Create a private-like name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Use getattr with a default to handle missing attributes
        return getattr(obj, self.storage_name, None)
    
    def __set__(self, obj, value):
        # Use setattr to set the "private" attribute
        setattr(obj, self.storage_name, value)
    
    def __delete__(self, obj):
        if hasattr(obj, self.storage_name):
            delattr(obj, self.storage_name)

# Comparing the patterns
class StorageCompare:
    dict_storage = DictStorage("default")
    dict_attr = DictAttrStorage("dict_attr")
    convention = ConventionStorage()

# Memory management is different in each approach
print("Note on memory management:")
print("- Pattern 1 can leak memory if objects are garbage collected but not removed from dict")
print("- Pattern 2 breaks non-data descriptors by putting values in instance __dict__")
print("- Pattern 3 is most common but requires each descriptor to track its own name")

# Validation descriptors
print("\n3. Validation Descriptors")
class Validated:
    def __init__(self, name=None):
        self.name = name
        self.storage_name = None
    
    def __set_name__(self, owner, name):
        # This is called when the descriptor is defined in a class
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, None)

class TypeValidated(Validated):
    def __init__(self, name=None, expected_type=None):
        super().__init__(name)
        self.expected_type = expected_type
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be of type {self.expected_type.__name__}")
        setattr(obj, self.storage_name, value)

class RangeValidated(TypeValidated):
    def __init__(self, name=None, expected_type=None, min_value=None, max_value=None):
        super().__init__(name, expected_type)
        self.min_value = min_value
        self.max_value = max_value
    
    def __set__(self, obj, value):
        # First use parent validation (type check)
        super().__set__(obj, value)
        
        # Then do range validation
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")

class Person:
    name = TypeValidated(expected_type=str)
    age = RangeValidated(expected_type=int, min_value=0, max_value=150)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

try:
    person = Person("Alice", 30)
    print(f"Created person: {person.name}, age {person.age}")
    
    # Test validations
    person.age = 35
    print(f"Updated age: {person.age}")
    
    # This should fail - wrong type
    person.name = 42
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

try:
    # This should fail - out of range
    person.age = 200
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

# Unit conversion descriptor
print("\n4. Unit Conversion Descriptor")
class UnitConverter:
    def __init__(self, unit_from, unit_to, conversion_factor):
        self.unit_from = unit_from
        self.unit_to = unit_to
        self.conversion_factor = conversion_factor
        self.storage_name = None
    
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Return the stored value (in original units)
        return getattr(obj, self.storage_name, 0)
    
    def __set__(self, obj, value):
        setattr(obj, self.storage_name, value)
    
    def convert(self, obj):
        # Get the value and convert it
        value = self.__get__(obj, type(obj))
        return value * self.conversion_factor

class Temperature:
    celsius = UnitConverter("C", "F", 1.0)  # Base unit
    
    def __init__(self, celsius=0):
        self.celsius = celsius
    
    @property
    def fahrenheit(self):
        # Convert from Celsius to Fahrenheit
        return self.celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        # Convert from Fahrenheit to Celsius
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(f"Temperature: {temp.celsius}°C = {temp.fahrenheit}°F")
temp.fahrenheit = 68
print(f"Updated temperature: {temp.celsius}°C = {temp.fahrenheit}°F")

# Lazy evaluation descriptor
print("\n5. Lazy Evaluation Descriptor")
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Compute the value and store it in the instance dict
        value = self.func(obj)
        obj.__dict__[self.name] = value  # Replace descriptor with value for this instance
        return value

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    @LazyProperty
    def sorted_data(self):
        print("Computing sorted data (expensive operation)")
        import time
        time.sleep(0.1)  # Simulate expensive computation
        return sorted(self.data)
    
    @LazyProperty
    def stats(self):
        print("Computing statistics (expensive operation)")
        sorted_data = self.sorted_data  # This will trigger the lazy property
        return {
            'min': sorted_data[0],
            'max': sorted_data[-1],
            'mean': sum(sorted_data) / len(sorted_data)
        }

processor = DataProcessor([5, 3, 8, 1, 9, 2, 7])
print(f"Created DataProcessor (no computation yet)")
print(f"Accessing sorted_data first time: {processor.sorted_data[:3]}...")
print(f"Accessing sorted_data second time: {processor.sorted_data[:3]}...")
print(f"Accessing stats: {processor.stats}")

# Descriptor for method binding
print("\n6. Method Binding Descriptor")
class BoundMethodDescriptor:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Return a bound method - function with 'self' already filled in
        def bound_method(*args, **kwargs):
            return self.func(obj, *args, **kwargs)
        
        bound_method.__name__ = self.func.__name__
        bound_method.__doc__ = self.func.__doc__
        return bound_method

class MyClass:
    def __init__(self, value):
        self.value = value
    
    @BoundMethodDescriptor
    def print_value(self):
        """Print the object's value"""
        print(f"Value: {self.value}")
    
    @BoundMethodDescriptor
    def add_to_value(self, amount):
        """Add the specified amount to the value"""
        self.value += amount
        return self.value

obj = MyClass(10)
obj.print_value()
print(f"New value after adding 5: {obj.add_to_value(5)}")

# Descriptor composition
print("\n7. Descriptor Composition")
class ValidatedProperty:
    def __init__(self, *validators):
        self.validators = validators
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, None)
    
    def __set__(self, obj, value):
        # Run all validators
        for validator in self.validators:
            value = validator(self.name, value)
        
        # Store the validated value
        setattr(obj, self.storage_name, value)

# Create validator functions
def type_validator(expected_type):
    def validate(name, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be of type {expected_type.__name__}")
        return value
    return validate

def range_validator(min_value=None, max_value=None):
    def validate(name, value):
        if min_value is not None and value < min_value:
            raise ValueError(f"{name} must be >= {min_value}")
        if max_value is not None and value > max_value:
            raise ValueError(f"{name} must be <= {max_value}")
        return value
    return validate

def string_validator(min_length=None, max_length=None):
    def validate(name, value):
        if min_length is not None and len(value) < min_length:
            raise ValueError(f"{name} must be at least {min_length} characters")
        if max_length is not None and len(value) > max_length:
            raise ValueError(f"{name} must be at most {max_length} characters")
        return value
    return validate

class User:
    name = ValidatedProperty(
        type_validator(str),
        string_validator(min_length=2, max_length=50)
    )
    
    age = ValidatedProperty(
        type_validator(int),
        range_validator(min_value=0, max_value=120)
    )
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

try:
    user = User("Alice", 30)
    print(f"Created user: {user.name}, age {user.age}")
    
    # This will fail validation
    user.name = "A"  # Too short
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

# Real-world example: SQLAlchemy-inspired field descriptors
print("\n8. Real-world Example: ORM Field Descriptors")
class Field:
    def __init__(self, column_type, primary_key=False, nullable=True, default=None):
        self.column_type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        
        # These will be set when the descriptor is assigned to a class
        self.name = None
        self.storage_name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"
        
        # Register this field with the model class
        if not hasattr(owner, '_fields'):
            owner._fields = {}
        owner._fields[name] = self
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, self.default)
    
    def __set__(self, obj, value):
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} cannot be null")
        
        # Validate type if a value is provided
        if value is not None and not isinstance(value, self.column_type):
            raise TypeError(f"{self.name} must be of type {self.column_type.__name__}")
        
        setattr(obj, self.storage_name, value)

class Model:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        fields = getattr(self.__class__, '_fields', {})
        values = [f"{name}={getattr(self, name)!r}" for name in fields]
        return f"{self.__class__.__name__}({', '.join(values)})"
    
    @classmethod
    def create_table_sql(cls):
        """Generate SQL to create a table for this model."""
        fields = getattr(cls, '_fields', {})
        if not fields:
            raise ValueError("No fields defined")
        
        columns = []
        for name, field in fields.items():
            column_type = field.column_type.__name__.upper()
            constraints = []
            if field.primary_key:
                constraints.append("PRIMARY KEY")
            if not field.nullable:
                constraints.append("NOT NULL")
            
            column_def = f"{name} {column_type}"
            if constraints:
                column_def += f" {' '.join(constraints)}"
            columns.append(column_def)
        
        table_name = cls.__name__.lower()
        return f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(columns) + "\n);"

class User(Model):
    id = Field(int, primary_key=True)
    name = Field(str, nullable=False)
    email = Field(str, nullable=False)
    age = Field(int, default=0)

user = User(id=1, name="Bob", email="bob@example.com")
print(f"User: {user}")
print(f"SQL to create table:\n{User.create_table_sql()}")