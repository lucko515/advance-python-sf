import sqlite3
import os
from datetime import datetime

# Create a database directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# What is SQLite?
print("\n1. What is SQLite?")
print("SQLite is a C library that provides a lightweight disk-based database")
print("that doesn't require a separate server process and allows accessing")
print("the database using a nonstandard variant of the SQL query language.")

print("\n2. When to use SQLite:")
use_cases = [
    "Embedded applications",
    "Local/client storage",
    "Prototyping and testing",
    "Low to medium traffic websites",
    "Data analysis and scientific applications",
    "One-off scripts and small tools"
]
for i, case in enumerate(use_cases, 1):
    print(f"   {i}. {case}")

# Connect to a database (creates it if it doesn't exist)
print("\n3. Creating/connecting to a database:")
db_path = "data/example.db"
conn = sqlite3.connect(db_path)
print(f"   - Connected to database at: {os.path.abspath(db_path)}")

# Creating a cursor
print("\n4. Creating a cursor for database operations:")
cursor = conn.cursor()
print("   - Cursor created for executing SQL commands")

# Creating a table
print("\n5. Creating a table:")
create_table_sql = '''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    hire_date TEXT
)
'''
cursor.execute(create_table_sql)
print("   - Created 'employees' table with columns: id, name, department, salary, hire_date")

# Inserting data
print("\n6. Inserting data:")
# Sample employee data
employees = [
    ("Alice Smith", "Engineering", 85000.00, datetime.now().strftime("%Y-%m-%d")),
    ("Bob Johnson", "Marketing", 72000.00, datetime.now().strftime("%Y-%m-%d")),
    ("Carol Williams", "Engineering", 92000.00, datetime.now().strftime("%Y-%m-%d")),
    ("Dave Brown", "HR", 65000.00, datetime.now().strftime("%Y-%m-%d")),
    ("Eve Davis", "Engineering", 110000.00, datetime.now().strftime("%Y-%m-%d"))
]

# Method 1: Execute many inserts at once
cursor.execute("DELETE FROM employees")  # Clear any existing data
cursor.executemany(
    "INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
    employees
)
print(f"   - Inserted {len(employees)} records using executemany()")

# Method 2: Individual inserts
print("   - Example of single insert with named parameters:")
cursor.execute(
    "INSERT INTO employees (name, department, salary, hire_date) VALUES (:name, :dept, :salary, :date)",
    {"name": "Frank Miller", "dept": "Sales", "salary": 78500.00, "date": datetime.now().strftime("%Y-%m-%d")}
)

# Committing changes
conn.commit()
print("   - Changes committed to database")

# Reading data
print("\n7. Querying data:")
print("   - Basic SELECT:")
cursor.execute("SELECT * FROM employees LIMIT 3")
rows = cursor.fetchall()
for row in rows:
    print(f"      {row}")

print("\n   - Filtered SELECT:")
cursor.execute("SELECT name, salary FROM employees WHERE department = ?", ("Engineering",))
engineering_staff = cursor.fetchall()
print(f"      Engineering staff ({len(engineering_staff)} employees):")
for person in engineering_staff:
    print(f"      {person[0]}: ${person[1]:.2f}")

# Updating data
print("\n8. Updating data:")
cursor.execute(
    "UPDATE employees SET salary = salary * 1.10 WHERE department = ?",
    ("Engineering",)
)
conn.commit()
print("   - Gave engineering department a 10% raise")

# Verify the update
cursor.execute("SELECT name, salary FROM employees WHERE department = ?", ("Engineering",))
updated_engineering = cursor.fetchall()
print("   - Updated engineering salaries:")
for person in updated_engineering:
    print(f"      {person[0]}: ${person[1]:.2f}")

# Deleting data
print("\n9. Deleting data:")
cursor.execute("DELETE FROM employees WHERE name = ?", ("Dave Brown",))
conn.commit()
print("   - Deleted employee: Dave Brown")

# Transaction example
print("\n10. Using transactions:")
try:
    # Start transaction
    cursor.execute("BEGIN TRANSACTION")
    
    # Multiple operations that should be atomic
    cursor.execute("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
                  ("Grace Lee", "Finance", 95000.00, datetime.now().strftime("%Y-%m-%d")))
    
    cursor.execute("UPDATE employees SET department = ? WHERE name = ?",
                  ("Finance", "Bob Johnson"))
    
    # Simulate an error
    # Uncommenting the next line would cause the transaction to rollback
    # raise Exception("Simulated error")
    
    # Commit changes if no errors
    cursor.execute("COMMIT")
    print("   - Transaction completed successfully")
    
except Exception as e:
    # Rollback on error
    cursor.execute("ROLLBACK")
    print(f"   - Transaction rolled back due to error: {e}")

# Clean up
cursor.close()
conn.close()
print("\n11. Connection closed")