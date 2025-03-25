# 02: Introduction to Metaclasses
print("Introduction to Metaclasses")
print("--------------------------")

# Classes are objects, created by the 'type' metaclass
print("1. Classes are objects, created by the 'type' metaclass")
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, my name is {self.name}"

print(f"Person is an instance of: {type(Person)}")
print(f"Person is a subclass of object: {issubclass(Person, object)}")

# Creating a class using type() directly
print("\n2. Creating a class using type() directly")
# type(name, bases, attributes)
def init_method(self, name):
    self.name = name

def greet_method(self):
    return f"Hello, my name is {self.name}"

# Create a class using type()
DynamicPerson = type(
    'DynamicPerson',  # Name of the class
    (object,),        # Base classes
    {
        '__init__': init_method,
        'greet': greet_method,
        'species': 'Human'
    }
)

# Use the dynamically created class
dynamic_person = DynamicPerson("Bob")
print(f"DynamicPerson type: {type(DynamicPerson)}")
print(f"dynamic_person.greet(): {dynamic_person.greet()}")
print(f"dynamic_person.species: {dynamic_person.species}")

# Creating a custom metaclass
print("\n3. Creating a custom metaclass")
class Meta(type):
    # Called when the metaclass is called to create a class
    def __new__(mcs, name, bases, attrs):
        print(f"Meta.__new__ creating class: {name}")
        # Add a class attribute to every class created with this metaclass
        attrs['metaclass_created'] = True
        # Call the parent metaclass's __new__ to create the class
        return super().__new__(mcs, name, bases, attrs)
    
    # Called after the class is created
    def __init__(cls, name, bases, attrs):
        print(f"Meta.__init__ initializing class: {name}")
        super().__init__(name, bases, attrs)
    
    # Called when the class is called to create an instance
    def __call__(cls, *args, **kwargs):
        print(f"Meta.__call__ creating instance of: {cls.__name__}")
        # Call the parent metaclass's __call__ to create the instance
        return super().__call__(*args, **kwargs)

# Use the metaclass to create a class
class MyClass(metaclass=Meta):
    def __init__(self, value):
        print(f"MyClass.__init__ called with value: {value}")
        self.value = value

# Create an instance of the class
print("\nCreating an instance of MyClass:")
obj = MyClass(42)

print(f"\nMyClass.metaclass_created: {MyClass.metaclass_created}")
print(f"obj.value: {obj.value}")

# Metaclass inheritance
print("\n4. Metaclass inheritance")
class ChildClass(MyClass):
    pass

print(f"ChildClass type: {type(ChildClass)}")  # Will be Meta
print(f"ChildClass.metaclass_created: {ChildClass.metaclass_created}")

# Metaclass that modifies methods
print("\n5. Metaclass that modifies methods")
class MethodModifierMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Modify all methods to have logging
        for attr_name, attr_value in list(attrs.items()):
            if callable(attr_value) and not attr_name.startswith('__'):
                attrs[attr_name] = mcs.add_logging(attr_value)
        return super().__new__(mcs, name, bases, attrs)
    
    @staticmethod
    def add_logging(method):
        def wrapper(*args, **kwargs):
            print(f"Calling method: {method.__name__}")
            result = method(*args, **kwargs)
            print(f"Method {method.__name__} returned: {result}")
            return result
        return wrapper

class ServiceWithLogging(metaclass=MethodModifierMeta):
    def process(self, data):
        return f"Processed {data}"
    
    def analyze(self, data):
        return f"Analyzed {data}"

print("\nUsing class with modified methods:")
service = ServiceWithLogging()
service.process("sample data")
service.analyze("other data")

# Use cases for metaclasses
print("\n6. Common use cases for metaclasses")

# Example: Registry pattern with metaclasses
print("\n7. Example: Registry pattern")
class PluginRegistry(type):
    plugins = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Don't register the base class
        if name != 'Plugin':
            mcs.plugins[name] = cls
        return cls

class Plugin(metaclass=PluginRegistry):
    def run(self):
        raise NotImplementedError("Plugins must implement run()")

class AudioPlugin(Plugin):
    def run(self):
        return "Running audio plugin"

class VideoPlugin(Plugin):
    def run(self):
        return "Running video plugin"

print(f"Registered plugins: {list(PluginRegistry.plugins.keys())}")
print(f"Creating and running a plugin: {PluginRegistry.plugins['AudioPlugin']().run()}")

"""\n--- Exercise ---
1. Create a metaclass that adds a class method `info()` to every class it creates."""
