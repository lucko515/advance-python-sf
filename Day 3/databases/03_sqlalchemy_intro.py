import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, Date

# Create a database directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# What is an ORM?
print("\n1. What is an ORM (Object-Relational Mapping)?")
print("   An ORM is a programming technique that converts data between")
print("   incompatible type systems in object-oriented programming languages.")
print("   It creates a 'virtual object database' that can be used from within")
print("   the programming language, eliminating the need for SQL in many cases.")

# Introducing SQLAlchemy
print("\n3. What is SQLAlchemy?")
print("   SQLAlchemy is the most popular and feature-rich SQL toolkit and ORM for Python.")
print("   It provides a full suite of well-known enterprise-level persistence patterns,")
print("   designed for efficient and high-performing database access.")

# SQLAlchemy Architecture
print("\n4. SQLAlchemy Architecture:")
"""
    "SQLAlchemy ORM": "High-level object interface for database operations",
    "SQLAlchemy Core": "SQL expression language and engine system",
    "DBAPI": "Python's database API specification (e.g., sqlite3, psycopg2)",
    "Database": "The actual database server or file"
"""

# Setting up SQLAlchemy
print("\n5. Setting up SQLAlchemy:")

# Creating a database engine
print("\n   5.1 Creating a database engine")
db_path = os.path.abspath("data/sqlalchemy_example.db")
engine = create_engine(f"sqlite:///{db_path}", echo=False)
print(f"   - Engine created for SQLite database at: {db_path}")
print("   - Connection string format: dialect[+driver]://user:password@host/dbname")

# Examples of connection strings for different databases
connection_strings = {
    "SQLite (memory)": "sqlite:///:memory:",
    "SQLite (file)": "sqlite:///path/to/file.db",
    "PostgreSQL": "postgresql://username:password@localhost/dbname",
    "MySQL": "mysql://username:password@localhost/dbname",
    "Oracle": "oracle://username:password@localhost:1521/dbname",
    "MS SQL Server": "mssql+pyodbc://username:password@DSN_NAME"
}

# Core vs ORM
print("\n6. SQLAlchemy Core vs ORM:")

# Core example (SQL Expression Language)
print("\n   6.1 Core example (SQL Expression Language):")
print("   - Lower-level, closer to raw SQL but still database-agnostic")
print("   - Good for complex queries or when you need fine-grained control")

# Using Core to execute a simple query
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello, SQLAlchemy Core!' as message"))
    print(f"   - Result from Core query: {result.fetchone()[0]}")

# ORM example (using declarative base)
print("\n   6.2 ORM example (Declarative Base):")
print("   - Higher-level, more 'Pythonic' object-oriented interface")
print("   - Classes represent tables, instances represent rows")

# Create a base class for declarative models
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer)
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', age={self.age})>"

# Display the model definition
print("\n   Defined User model with SQLAlchemy ORM:")
print("   - Table name: users")
print("   - Columns: id, name, email, age")
print("   - The User class now represents the 'users' table in our database")

# Create all tables
print("\n7. Creating tables from models:")
Base.metadata.create_all(engine)
print("   - Created all tables defined in our models")

# Session management
print("\n8. Working with Sessions:")
print("   - Sessions manage ORM objects and their transactions")
print("   - Similar to a 'staging area' in git - changes are tracked but not committed immediately")

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
print("   - Created a new session bound to our database engine")

# Adding objects
print("\n9. Basic CRUD operations with the ORM:")
print("\n   9.1 Creating records (INSERT):")

# Create new users
new_users = [
    User(name="Alice Smith", email="alice@example.com", age=30),
    User(name="Bob Johnson", email="bob@example.com", age=25),
    User(name="Charlie Brown", email="charlie@example.com", age=35)
]

# Add users to the session
for user in new_users:
    session.add(user)

# Commit the session to persist changes
session.commit()
print(f"   - Added {len(new_users)} users to the database")

# Querying objects
print("\n   9.2 Reading records (SELECT):")
users = session.query(User).all()
print(f"   - Retrieved {len(users)} users from the database:")
for user in users:
    print(f"      {user}")

# Filtering queries
print("\n   9.3 Filtering queries:")
young_users = session.query(User).filter(User.age < 30).all()
print(f"   - Users under 30: {len(young_users)}")
for user in young_users:
    print(f"      {user}")

# Updating objects
print("\n   9.4 Updating records (UPDATE):")
user_to_update = session.query(User).filter_by(name="Alice Smith").first()
if user_to_update:
    print(f"   - Before update: {user_to_update}")
    user_to_update.age = 31
    session.commit()
    print(f"   - After update: {user_to_update}")

# Deleting objects
print("\n   9.5 Deleting records (DELETE):")
user_to_delete = session.query(User).filter_by(name="Charlie Brown").first()
if user_to_delete:
    print(f"   - Deleting: {user_to_delete}")
    session.delete(user_to_delete)
    session.commit()
    print("   - User deleted")

# Verify deletion
remaining_users = session.query(User).all()
print(f"   - Remaining users: {len(remaining_users)}")
for user in remaining_users:
    print(f"      {user}")

# Clean up
session.close()
print("\n10. Session closed")
