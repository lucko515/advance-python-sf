# 06: Property as a Descriptor
print("Property as a Descriptor")
print("----------------------")

# Basic property usage
print("1. Basic property Usage")
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        print("Getting radius")
        return self._radius
    
    @radius.setter
    def radius(self, value):
        print(f"Setting radius to {value}")
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def diameter(self):
        return self._radius * 2
    
    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

circle = Circle(5)
print(f"Radius: {circle.radius}")
print(f"Diameter: {circle.diameter}")
print(f"Area: {circle.area:.2f}")

circle.radius = 10
print(f"New radius: {circle.radius}")
print(f"New diameter: {circle.diameter}")

try:
    circle.radius = -5
except ValueError as e:
    print(f"Error: {e}")

# How property works as a descriptor
print("\n2. How property Works as a Descriptor")
print("property is a built-in descriptor that:")
print("- Uses __get__ to call your getter method")
print("- Uses __set__ to call your setter method")
print("- Uses __delete__ to call your deleter method")
print("- Manages the linking between these methods")

# Equivalent implementation without decorators
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def get_width(self):
        return self._width
    
    def set_width(self, value):
        if value < 0:
            raise ValueError("Width cannot be negative")
        self._width = value
    
    def get_height(self):
        return self._height
    
    def set_height(self, value):
        if value < 0:
            raise ValueError("Height cannot be negative")
        self._height = value
    
    def get_area(self):
        return self._width * self._height
    
    # Create properties using the property() constructor
    width = property(get_width, set_width, doc="Width of the rectangle")
    height = property(get_height, set_height, doc="Height of the rectangle")
    area = property(get_area, doc="Area of the rectangle")

rect = Rectangle(10, 5)
print(f"Width: {rect.width}, Height: {rect.height}, Area: {rect.area}")
rect.width = 20
print(f"New width: {rect.width}, New area: {rect.area}")

# Under the hood: Building a Property descriptor from scratch
print("\n3. Building a Custom Property Descriptor")
class CustomProperty:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget and fget.__doc__)
        # For method chaining with decorators
        self.name = None
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)
    
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

# Using our custom property
class Person:
    def __init__(self, name, age=0):
        self._name = name
        self._age = age
    
    @CustomProperty
    def name(self):
        """Person's name"""
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value
    
    @CustomProperty
    def age(self):
        """Person's age"""
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

person = Person("Alice", 30)
print(f"Name: {person.name}, Age: {person.age}")
person.name = "Bob"
person.age = 25
print(f"New name: {person.name}, New age: {person.age}")

# Inspecting property objects
print("\n4. Inspecting Property Objects")
class Demo:
    @property
    def value(self):
        return 42
    
    @value.setter
    def value(self, val):
        pass

# Get the property object from the class
prop = Demo.__dict__['value']
print(f"Type of property: {type(prop)}")
print(f"Property attributes: {dir(prop)[:10]} ...")
print(f"Property has __get__: {hasattr(prop, '__get__')}")
print(f"Property has __set__: {hasattr(prop, '__set__')}")

# Advanced property patterns
print("\n5. Advanced Property Patterns")

# Cached property pattern
class ExpensiveCalculation:
    def __init__(self, data):
        self.data = data
        # For manually tracking when to invalidate cache
        self._results_valid = {}
        # For storing computed results
        self._cache = {}
    
    def clear_cache(self):
        self._cache.clear()
        self._results_valid.clear()
    
    def invalidate(self, attr_name):
        self._results_valid[attr_name] = False
    
    @property
    def sorted_data(self):
        cache_key = 'sorted_data'
        if cache_key not in self._cache or not self._results_valid.get(cache_key, False):
            print("Computing sorted_data (expensive operation)")
            # Simulate expensive operation
            import time
            time.sleep(0.1)
            self._cache[cache_key] = sorted(self.data)
            self._results_valid[cache_key] = True
        return self._cache[cache_key]
    
    @property
    def stats(self):
        cache_key = 'stats'
        if cache_key not in self._cache or not self._results_valid.get(cache_key, False):
            print("Computing statistics (expensive operation)")
            # Use the cached sorted data if available
            sorted_data = self.sorted_data
            self._cache[cache_key] = {
                'min': sorted_data[0],
                'max': sorted_data[-1],
                'avg': sum(sorted_data) / len(sorted_data),
                'median': sorted_data[len(sorted_data) // 2]
            }
            self._results_valid[cache_key] = True
        return self._cache[cache_key]

calc = ExpensiveCalculation([5, 3, 8, 1, 9, 2, 7])
print(f"First access to sorted_data: {calc.sorted_data}")
print(f"Second access to sorted_data (should be cached): {calc.sorted_data}")
print(f"First access to stats: {calc.stats}")
print(f"Second access to stats (should be cached): {calc.stats}")

calc.data.append(10)  # Modify the underlying data
calc.invalidate('sorted_data')  # Mark cache as invalid
calc.invalidate('stats')  # Mark cache as invalid
print(f"After invalidating cache: {calc.sorted_data}")
print(f"Stats after invalidating: {calc.stats}")

# Property factory pattern
print("\n6. Property Factory Pattern")
def validated_property(name, expected_type, validator=None):
    storage_name = f"_{name}"
    
    @property
    def prop(self):
        return getattr(self, storage_name)
    
    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be of type {expected_type.__name__}")
        if validator and not validator(value):
            raise ValueError(f"{name} failed validation")
        setattr(self, storage_name, value)
    
    return prop

class Product:
    # Create properties with validation using the factory
    name = validated_property("name", str, lambda x: len(x) > 0)
    price = validated_property("price", (int, float), lambda x: x >= 0)
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

try:
    product = Product("Laptop", 999.99)
    print(f"Product: {product.name}, ${product.price}")
    
    # This will fail validation
    product.price = -50
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

# Class properties (shared between all instances)
print("\n7. Class Properties")
class ClassPropertyDescriptor:
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset
    
    def __get__(self, obj, objtype=None):
        # Always use the class, not the instance
        return self.fget(objtype)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        # Set on the class, not the instance
        self.fset(obj.__class__, value)
    
    def setter(self, func):
        return type(self)(self.fget, func)

# Decorator to create class properties
def classproperty(func):
    return ClassPropertyDescriptor(func)

class Database:
    _connection_string = "default_connection"
    _connection_count = 0
    
    def __init__(self):
        Database._connection_count += 1
    
    @classproperty
    def connection_string(cls):
        return cls._connection_string
    
    @connection_string.setter
    def connection_string(cls, value):
        cls._connection_string = value
    
    @classproperty
    def connection_count(cls):
        return cls._connection_count

# Create some instances
db1 = Database()
db2 = Database()

print(f"Connection string: {Database.connection_string}")
print(f"Connection string via instance: {db1.connection_string}")
print(f"Connection count: {Database.connection_count}")

# Change the class attribute
Database.connection_string = "mysql://root:password@localhost/db"
print(f"New connection string: {db1.connection_string}")
print(f"Connection string on different instance: {db2.connection_string}")

# Properties for attributes with dependencies
print("\n8. Properties with Dependencies")
class Rectangle:
    def __init__(self, width=0, height=0):
        # Use direct attribute access to avoid triggering setters during init
        self._width = width
        self._height = height
        self._area = width * height
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        # Update dependent attributes
        self._area = self._width * self._height
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        # Update dependent attributes
        self._area = self._width * self._height
    
    @property
    def area(self):
        return self._area

rect = Rectangle(10, 5)
print(f"Width: {rect.width}, Height: {rect.height}, Area: {rect.area}")
rect.width = 20
print(f"After changing width - Area: {rect.area}")