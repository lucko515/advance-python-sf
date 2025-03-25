# 05: The Descriptor Protocol
print("The Descriptor Protocol")
print("---------------------")

# Define what descriptors are
print("1. What are Descriptors?")
print("Descriptors are objects that implement the descriptor protocol:")
print("  - __get__(self, obj, type=None) -> value")
print("  - __set__(self, obj, value) -> None")
print("  - __delete__(self, obj) -> None")
print("They control how attributes are accessed on objects.")

# Basic descriptor example
print("\n2. Basic Descriptor Example")
class Verbose:
    # TODO:
    pass

class MyClass:
    # Descriptor instance is a class attribute
    attribute = Verbose()

obj = MyClass()
print(f"Accessing obj.attribute: {obj.attribute}")
obj.attribute = 100
print("Deleting obj.attribute...")
del obj.attribute

# How method descriptor works
print("\n3. How Python Methods Work (Function Descriptor)")
def show_descriptor_binding(obj, method_name):
    # Get the descriptor from the class
    descriptor = obj.__class__.__dict__[method_name]
    print(f"Descriptor: {descriptor}")
    
    # Get the bound method from the instance
    bound_method = getattr(obj, method_name)
    print(f"Bound method: {bound_method}")
    
    # Show that the bound method has reference to the instance
    print(f"Bound method's self: {bound_method.__self__}")

class Example:
    def method(self):
        return "method called"

# Functions in a class become methods due to a descriptor
example = Example()
show_descriptor_binding(example, "method")

# Understanding data descriptors vs non-data descriptors
print("\n4. Data Descriptors vs Non-data Descriptors")

class DataDescriptor:
    # TODO
    pass

class NonDataDescriptor:
    # TODO
    pass

class Demo:
    data_desc = DataDescriptor()
    non_data_desc = NonDataDescriptor()

demo = Demo()

# Original behavior
print(f"demo.data_desc: {demo.data_desc}")
print(f"demo.non_data_desc: {demo.non_data_desc}")

# Add instance attributes with the same names
demo.__dict__['data_desc'] = "instance data_desc"
demo.__dict__['non_data_desc'] = "instance non_data_desc"

# Check the behavior now
print(f"After adding to __dict__:")
print(f"demo.data_desc: {demo.data_desc}")  # Data descriptor still wins
print(f"demo.non_data_desc: {demo.non_data_desc}")  # Instance attribute wins

# The property descriptor
print("\n5. The property() Descriptor")
# How property would be implemented as a descriptor
class PropertyDescriptor:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc
    
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

# Using our custom property-like descriptor
class Person:
    def __init__(self, name=""):
        self._name = name
    
    def _get_name(self):
        print("Getting name")
        return self._name
    
    def _set_name(self, value):
        print(f"Setting name to {value}")
        self._name = value
    
    def _del_name(self):
        print("Deleting name")
        del self._name
    
    # Use our custom property descriptor
    name = PropertyDescriptor(_get_name, _set_name, _del_name, "Person's name")

p = Person("Alice")
print(f"p.name: {p.name}")
p.name = "Bob"
print(f"p.name after setting: {p.name}")

# Python's built-in property
print("\n6. Python's Built-in property() Decorator")
class Employee:
    def __init__(self, first="", last=""):
        self._first = first
        self._last = last
        self._email = None
    
    @property
    def first(self):
        return self._first
    
    @first.setter
    def first(self, value):
        self._first = value
        self._email = None  # Reset cached email
    
    @property
    def last(self):
        return self._last
    
    @last.setter
    def last(self, value):
        self._last = value
        self._email = None  # Reset cached email
    
    @property
    def email(self):
        if self._email is None:
            self._email = f"{self._first.lower()}.{self._last.lower()}@example.com"
        return self._email

emp = Employee("John", "Smith")
print(f"emp.first: {emp.first}")
print(f"emp.last: {emp.last}")
print(f"emp.email: {emp.email}")

emp.first = "Jane"
print(f"After changing first name, emp.email: {emp.email}")

# Descriptor for type validation
print("\n7. Type Validation Descriptor")
class Typed:
    #TODO
    pass

class TypedPerson:
    name = Typed("name", str)
    age = Typed("age", int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

try:
    person = TypedPerson("Alice", 30)
    print(f"Created person: {person.name}, {person.age}")
    
    # This should raise an error
    person.age = "thirty"
except TypeError as e:
    print(f"Error: {e}")

# Attribute lookup chain
print("\n8. Attribute Lookup Chain")

# Descriptors at class vs instance level
print("\n9. Descriptors at Class vs Instance Level")
class DescriptorDemo:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return f"Accessed through class: {objtype.__name__}"
        return f"Accessed through instance: {obj}"

class Test:
    x = DescriptorDemo()

# Access through instance
t = Test()
print(f"t.x: {t.x}")  # Descriptor.__get__(t, Test)

# Access through class
print(f"Test.x: {Test.x}")  # Descriptor.__get__(None, Test)

# Implementing a descriptor with memory of each instance's value
print("\n10. Per-instance State in Descriptors")
class InstanceStateDescriptor:
    def __init__(self, name):
        # Use the descriptor's name as the key in the instance __dict__
        self.storage_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Get the value from the instance __dict__
        return getattr(obj, self.storage_name, None)
    
    def __set__(self, obj, value):
        # Store the value in the instance __dict__
        setattr(obj, self.storage_name, value)

class StateDemo:
    x = InstanceStateDescriptor('x')
    y = InstanceStateDescriptor('y')
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

s1 = StateDemo(10, 20)
s2 = StateDemo(30, 40)

print(f"s1.x: {s1.x}, s1.y: {s1.y}")
print(f"s2.x: {s2.x}, s2.y: {s2.y}")

s1.x = 15
print(f"After s1.x = 15, s1.x: {s1.x}, s2.x: {s2.x}")

"""\n--- Exercise ---
1. Create a descriptor that enforces a range of valid values for an attribute."""
