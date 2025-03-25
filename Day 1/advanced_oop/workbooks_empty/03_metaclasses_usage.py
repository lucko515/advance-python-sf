# 03: Practical Metaclass Usage
print("Practical Metaclass Usage")
print("------------------------")

# 1. Validation metaclass: Enforcing class structure
print("1. Validation Metaclass")
class RequiredAttributesMeta(type):
    # TODO:
    pass

class ValidatedClass(metaclass=RequiredAttributesMeta):
    required_attrs = ['validate', 'process']

try:
    # This will fail - missing 'process' attribute
    class InvalidService(ValidatedClass):
        def validate(self):
            return True
        
    print("Created InvalidService class")
except TypeError as e:
    print(f"Error creating class: {e}")

# This will work - has all required attributes
class ValidService(ValidatedClass):
    def validate(self):
        return True
    
    def process(self):
        return "Processing data"

print(f"Successfully created ValidService class")

# 2. Singleton pattern using metaclass
print("\n2. Singleton Metaclass")
class SingletonMeta(type):
    # TODO
    pass

class ConfigManager(metaclass=SingletonMeta):
    def __init__(self, settings=None):
        self.settings = settings or {}
    
    def get_setting(self, key, default=None):
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        self.settings[key] = value

# Create two "instances" - should be the same object
config1 = ConfigManager({"debug": True})
config2 = ConfigManager()  # Should not reset settings

print(f"config1 settings: {config1.settings}")
print(f"config2 settings: {config2.settings}")
print(f"config1 is config2: {config1 is config2}")

config2.set_setting("logging", "verbose")
print(f"After updating config2, config1 settings: {config1.settings}")

# 3. Auto-registering subclasses (e.g., for plugins, serializers, etc.)
print("\n3. Auto-registering Subclasses")
class RegisterMeta(type):
    registry = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Don't register abstract base classes
        if not getattr(cls, 'abstract', False):
            # Register class by format name or class name
            key = getattr(cls, 'format_name', name)
            mcs.registry[key] = cls
        return cls
    
    @classmethod
    def get_converter(mcs, format_name):
        return mcs.registry.get(format_name)

class DataConverter(metaclass=RegisterMeta):
    abstract = True
    
    def convert(self, data):
        raise NotImplementedError("Subclasses must implement convert()")

class JSONConverter(DataConverter):
    format_name = 'json'
    
    def convert(self, data):
        return f"Converting {data} to JSON"

class XMLConverter(DataConverter):
    format_name = 'xml'
    
    def convert(self, data):
        return f"Converting {data} to XML"

class CSVConverter(DataConverter):
    # Uses class name as format_name
    def convert(self, data):
        return f"Converting {data} to CSV"

print(f"Registered converters: {list(RegisterMeta.registry.keys())}")

# Get converter by format name
json_converter = RegisterMeta.get_converter('json')
print(f"json_converter: {json_converter().convert('data')}")

# 4. Attribute access modification using metaclass __getattribute__
print("\n4. Attribute Access Modification")
class LazyAttributeMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Convert all _lazy_X attributes to properties
        for attr_name, attr_value in list(attrs.items()):
            if attr_name.startswith('_lazy_'):
                property_name = attr_name[6:]  # remove '_lazy_'
                attrs[property_name] = mcs.make_property(attr_name)
        
        return super().__new__(mcs, name, bases, attrs)
    
    @staticmethod
    def make_property(lazy_attr):
        def getter(self):
            # If not yet cached, compute and cache it
            if not hasattr(self, f"_cache_{lazy_attr}"):
                result = getattr(self, lazy_attr)()
                setattr(self, f"_cache_{lazy_attr}", result)
            return getattr(self, f"_cache_{lazy_attr}")
        
        return property(getter)

class ExpensiveOperations(metaclass=LazyAttributeMeta):
    def __init__(self, data):
        self.data = data
    
    def _lazy_processed_data(self):
        print("Computing processed_data (expensive operation)...")
        # Simulate expensive computation
        return [x * 2 for x in self.data]
    
    def _lazy_stats(self):
        print("Computing statistics (expensive operation)...")
        # Simulate expensive computation
        data = self.processed_data  # Uses the property, which may be cached
        return {
            "sum": sum(data),
            "len": len(data),
            "avg": sum(data) / len(data) if data else 0
        }

ops = ExpensiveOperations([1, 2, 3, 4, 5])
print("Object created, no computation yet")

print("\nAccessing processed_data first time:")
print(f"Processed data: {ops.processed_data}")

print("\nAccessing processed_data second time (should use cache):")
print(f"Processed data: {ops.processed_data}")

print("\nAccessing stats (should use cached processed_data):")
print(f"Stats: {ops.stats}")

# 5. Django-inspired model field system
print("\n5. Class Attribute Collection and Processing")
class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Collect field definitions
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                # Store field and remove from class namespace
                fields[key] = value
                # Set the field name to the attribute name
                value.name = key
        
        # Store fields on the class
        attrs['_fields'] = fields
        
        return super().__new__(mcs, name, bases, attrs)

class Field:
    def __init__(self, field_type, required=True, default=None):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.name = None  # Set by metaclass
    
    def validate(self, value):
        if value is None:
            if self.required:
                raise ValueError(f"Field {self.name} is required")
            return self.default
        
        if not isinstance(value, self.field_type):
            raise TypeError(f"Field {self.name} must be of type {self.field_type.__name__}")
        
        return value

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        # Set attributes based on fields
        for name, field in self._fields.items():
            value = kwargs.get(name)
            setattr(self, name, field.validate(value))
    
    def __repr__(self):
        attrs = ", ".join(f"{name}={getattr(self, name)!r}" for name in self._fields)
        return f"{self.__class__.__name__}({attrs})"

class User(Model):
    name = Field(str)
    age = Field(int, required=False, default=0)
    email = Field(str)

try:
    # This will work
    user1 = User(name="Alice", email="alice@example.com")
    print(f"Created user: {user1}")
    
    # This will fail - missing required email
    user2 = User(name="Bob")
    print(f"Created user: {user2}")
except (ValueError, TypeError) as e:
    print(f"Error creating user: {e}")

# Try with invalid field type
try:
    user3 = User(name="Charlie", email="charlie@example.com", age="thirty")
    print(f"Created user: {user3}")
except (ValueError, TypeError) as e:
    print(f"Error creating user: {e}")

"--- Exercise --- 1. Extend the Singleton metaclass to allow parameterized instances (e.g., a connection pool with different names)."
