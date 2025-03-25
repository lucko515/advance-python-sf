# 09: Practical Real-world Examples
print("Practical Real-world Examples")
print("---------------------------")

# Django-inspired models system
print("1. Django-inspired Models System")
print("Django uses metaclasses and descriptors for its ORM model declaration.\n")

class Field:
    """Base field class for model attributes."""
    def __init__(self, name=None, primary_key=False, max_length=None, null=False, default=None):
        self.name = name
        self.primary_key = primary_key
        self.max_length = max_length
        self.null = null
        self.default = default
    
    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name, self.default)
    
    def __set__(self, instance, value):
        instance._data[self.name] = value
    
    def db_type(self):
        """Return the database column type for this field."""
        raise NotImplementedError("Subclasses must implement db_type()")

class CharField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(max_length=max_length, **kwargs)
    
    def db_type(self):
        return f"VARCHAR({self.max_length})"

class IntegerField(Field):
    def db_type(self):
        return "INTEGER"

class BooleanField(Field):
    def db_type(self):
        return "BOOLEAN"

class ModelBase(type):
    """Metaclass for Django-like models."""
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)
        
        # Create a new class
        cls = super().__new__(mcs, name, bases, attrs)
        
        # Add a table name
        if not hasattr(cls, 'Meta') or not hasattr(cls.Meta, 'table_name'):
            cls._table_name = name.lower()
        else:
            cls._table_name = cls.Meta.table_name
        
        # Collect fields
        cls._fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                cls._fields[key] = value
        
        return cls

class Model(metaclass=ModelBase):
    """Base model class for Django-like models."""
    def __init__(self, **kwargs):
        self._data = {}
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self, key, value)
    
    def __repr__(self):
        values = []
        for name in self._fields:
            values.append(f"{name}={getattr(self, name, None)!r}")
        return f"{self.__class__.__name__}({', '.join(values)})"
    
    @classmethod
    def create_table_sql(cls):
        """Generate SQL to create a table for this model."""
        columns = []
        for name, field in cls._fields.items():
            column_def = f"{name} {field.db_type()}"
            if field.primary_key:
                column_def += " PRIMARY KEY"
            if not field.null:
                column_def += " NOT NULL"
            columns.append(column_def)
        
        return f"CREATE TABLE {cls._table_name} (\n  " + ",\n  ".join(columns) + "\n);"

# Using the Django-inspired models
class Post(Model):
    class Meta:
        table_name = "blog_posts"
    
    title = CharField(max_length=100, null=False)
    content = CharField(max_length=1000, null=False)
    published = BooleanField(default=False)
    views = IntegerField(default=0)

post = Post(title="Hello, World!", content="This is my first post", published=True)
print(f"Post: {post}")
print(f"SQL to create table:\n{Post.create_table_sql()}")

# SQLAlchemy-inspired declarative system
print("\n2. SQLAlchemy-inspired Declarative System")
print("SQLAlchemy uses metaclasses and descriptors for its declarative model system.\n")

class Column:
    """SQLAlchemy-like column descriptor."""
    def __init__(self, type_, primary_key=False, nullable=True):
        self.type_ = type_
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._values.get(self.name)
    
    def __set__(self, instance, value):
        instance._values[self.name] = value

class Table:
    """Represents a database table."""
    def __init__(self, name, *columns):
        self.name = name
        self.columns = columns

class DeclarativeMeta(type):
    """Metaclass for SQLAlchemy-like declarative models."""
    def __new__(mcs, name, bases, attrs):
        if name == 'Base':
            return super().__new__(mcs, name, bases, attrs)
        
        # Create a new class
        cls = super().__new__(mcs, name, bases, attrs)
        
        # Add a table
        tablename = attrs.get('__tablename__', name.lower())
        columns = []
        
        for key, value in attrs.items():
            if isinstance(value, Column):
                columns.append((key, value))
        
        cls.__table__ = Table(tablename, *columns)
        
        return cls

class Base(metaclass=DeclarativeMeta):
    """Base class for SQLAlchemy-like models."""
    def __init__(self, **kwargs):
        self._values = {}
        for key, value in kwargs.items():
            if hasattr(self.__class__, key) and isinstance(getattr(self.__class__, key), Column):
                setattr(self, key, value)
    
    def __repr__(self):
        values = []
        for key, _ in self.__table__.columns:
            value = getattr(self, key, None)
            values.append(f"{key}={value!r}")
        return f"{self.__class__.__name__}({', '.join(values)})"

# Using the SQLAlchemy-inspired declarative system
class User(Base):
    __tablename__ = "users"
    
    id = Column(int, primary_key=True)
    name = Column(str, nullable=False)
    email = Column(str, nullable=False)
    is_active = Column(bool, nullable=False)

user = User(id=1, name="Alice", email="alice@example.com", is_active=True)
print(f"User: {user}")
print(f"Table name: {user.__table__.name}")
print(f"Columns: {[col[0] for col in user.__table__.columns]}")

# Flask-inspired routing system
print("\n3. Flask-inspired Routing System")
print("Flask uses decorators for its routing system.\n")

class FlaskApp:
    """Simplified Flask application."""
    def __init__(self, name):
        self.name = name
        self.routes = {}
    
    def route(self, path, methods=None):
        """Decorator to register a route function."""
        methods = methods or ['GET']
        
        def decorator(func):
            self.routes[(path, tuple(methods))] = func
            return func
        
        return decorator
    
    def get(self, path):
        """Decorator for GET routes."""
        return self.route(path, methods=['GET'])
    
    def post(self, path):
        """Decorator for POST routes."""
        return self.route(path, methods=['POST'])
    
    def handle_request(self, path, method, **kwargs):
        """Simulates handling a request."""
        route_key = (path, (method,))
        if route_key not in self.routes:
            return f"404 Not Found: {path} [{method}]"
        
        handler = self.routes[route_key]
        return handler(**kwargs)
    
    def __repr__(self):
        routes = []
        for (path, methods), func in self.routes.items():
            routes.append(f"{func.__name__} -> {path} {methods}")
        return f"FlaskApp(name={self.name!r}, routes=[\n  " + "\n  ".join(routes) + "\n])"

# Using the Flask-inspired routing system
app = FlaskApp("MyApp")

@app.route("/", methods=["GET"])
def index():
    return "Welcome to the home page!"

@app.get("/users")
def get_users():
    return "List of users"

@app.post("/users")
def create_user():
    return "User created"

print(f"App: {app}")
print(f"Handling GET /: {app.handle_request('/', 'GET')}")
print(f"Handling GET /users: {app.handle_request('/users', 'GET')}")
print(f"Handling POST /users: {app.handle_request('/users', 'POST')}")
print(f"Handling GET /invalid: {app.handle_request('/invalid', 'GET')}")