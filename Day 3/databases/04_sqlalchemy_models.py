import os
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy import CheckConstraint, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

# Create a database directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Create SQLAlchemy engine and base
db_path = os.path.abspath("data/sqlalchemy_models.db")
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base = declarative_base()

# Available Column Types
print("\n1. Common SQLAlchemy Column Types:")
column_types = {
    "Integer": "Whole numbers (mapped to INT in most databases)",
    "String": "Variable-length strings (VARCHAR in SQL)",
    "Text": "Unlimited length text (TEXT in SQL)",
    "Float": "Floating point numbers",
    "Numeric": "Fixed precision numbers (e.g., for currency)",
    "Boolean": "True/False values",
    "Date": "Date values without time",
    "DateTime": "Date and time values",
    "Time": "Time values without date",
    "Enum": "A set of string values",
    "JSON": "JSON formatted data (if supported by database)",
    "LargeBinary": "Binary data (BLOB in SQL)",
    "PickleType": "Automatic pickling/unpickling of Python objects",
    "Interval": "Time intervals"
}


print("\n2. Column Constraints and Options:")
constraints = {
    "primary_key=True": "Designates the column as the primary key",
    "nullable=False": "Column cannot contain NULL values",
    "unique=True": "All values in column must be unique",
    "index=True": "Create an index on this column",
    "default=value": "Default value if none is provided",
    "server_default=text": "Default value set by the database server",
    "onupdate=func": "Function to call when updating the row",
    "doc='text'": "Documentation string for the column"
}

# Defining models
print("\n3. Defining SQLAlchemy Models:")

# Example 1: Basic model
print("\n   3.1 Basic Model Example:")
class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.first_name} {self.last_name}')>"

print("   Customer model defined with columns:")
print("   - id (primary key)")
print("   - first_name (required)")
print("   - last_name (required)")
print("   - email (required, unique)")
print("   - active (defaults to True)")
print("   - created_at (defaults to current time)")
print("   - notes (optional text)")

# Example 2: Model with constraints
print("\n   3.2 Model with Table-Level Constraints:")
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sku = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Table-level constraints
    __table_args__ = (
        UniqueConstraint('sku', name='uix_product_sku'),
        CheckConstraint('price > 0', name='ck_product_price_positive'),
        Index('ix_product_name', 'name'),
    )
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price=${self.price:.2f})>"

print("   Product model defined with additional table-level constraints:")
print("   - UniqueConstraint on SKU")
print("   - CheckConstraint to ensure price is positive")
print("   - Index on product name for faster lookups")
print("   - Updated_at column that auto-updates on changes")

# Example 3: Model with custom primary key
print("\n   3.3 Model with Custom Primary Key Strategy:")
class ConfigSetting(Base):
    __tablename__ = 'config_settings'
    
    # Using a string as the primary key
    key = Column(String(50), primary_key=True)
    value = Column(String(255))
    description = Column(Text)
    is_secret = Column(Boolean, default=False)
    
    def __repr__(self):
        if self.is_secret:
            return f"<ConfigSetting(key='{self.key}', value='*****')>"
        return f"<ConfigSetting(key='{self.key}', value='{self.value}')>"

print("   ConfigSetting model with a string-based primary key:")
print("   - Primary key is 'key' (string) instead of auto-incremented integer")
print("   - Simple key-value storage pattern")
print("   - Support for marking some values as secret")

# Create tables in the database
Base.metadata.create_all(engine)
print("\n4. Created all database tables from models")

# Inspecting the database schema
print("\n5. Database Schema Inspection:")
inspector = inspect(engine)
table_names = inspector.get_table_names()
print(f"   Database contains {len(table_names)} tables:")
for table_name in table_names:
    print(f"\n   Table: {table_name}")
    print("   Columns:")
    for column in inspector.get_columns(table_name):
        print(f"   - {column['name']}: {column['type']} (nullable: {column['nullable']})")
    
    primary_keys = inspector.get_primary_keys(table_name)
    if primary_keys:
        print(f"   Primary key(s): {', '.join(primary_keys)}")
    
    foreign_keys = inspector.get_foreign_keys(table_name)
    if foreign_keys:
        for fk in foreign_keys:
            print(f"   Foreign key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    
    indices = inspector.get_indexes(table_name)
    if indices:
        for index in indices:
            print(f"   Index: {index['name']} on {index['column_names']} (unique: {index['unique']})")

# Saving sample data
print("\n6. Adding sample data to models:")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample customers
customers = [
    Customer(first_name="John", last_name="Smith", email="john@example.com", 
             notes="Regular customer"),
    Customer(first_name="Emma", last_name="Johnson", email="emma@example.com", 
             notes="Premium member"),
    Customer(first_name="Michael", last_name="Davis", email="michael@example.com", 
             active=False, notes="Inactive account")
]

# Sample products
products = [
    Product(name="Laptop", sku="TECH-1001", price=1299.99, 
            description="High-performance laptop for professionals"),
    Product(name="Smartphone", sku="TECH-2001", price=799.99, 
            description="Latest smartphone model"),
    Product(name="Wireless Headphones", sku="TECH-3001", price=149.99, 
            description="Noise-cancelling wireless headphones")
]

# Sample config settings
config_settings = [
    ConfigSetting(key="app.name", value="SQLAlchemy Demo", 
                  description="Application name"),
    ConfigSetting(key="app.debug", value="False", 
                  description="Debug mode flag"),
    ConfigSetting(key="db.connection_timeout", value="30", 
                  description="Database connection timeout in seconds"),
    ConfigSetting(key="api.secret_key", value="sk_test_abcdefghijklmnopqrstuv", 
                  description="API secret key", is_secret=True)
]

# Add all objects to the session
for customer in customers:
    session.add(customer)
    
for product in products:
    session.add(product)
    
for setting in config_settings:
    session.add(setting)

# Commit the session
session.commit()
print(f"   Added {len(customers)} customers, {len(products)} products, and {len(config_settings)} config settings")

# Clean up
session.close()
print("\n7. Session closed")