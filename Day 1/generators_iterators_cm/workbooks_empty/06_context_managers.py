# 06: Context Managers
print("Context Managers")
print("---------------")



# Creating a simple file to use in examples
with open("example.txt", "w") as file:
    file.write("This is a test file created for context manager examples.\n")
    file.write("Line 2\nLine 3\nLine 4\nLine 5")

# Demo of with statement for file handling
print("\nDemonstrating file handling with context manager:")
with open("example.txt", "r") as file:
    first_line = file.readline()
    print(f"  First line: {first_line.strip()}")
    second_line = file.readline()
    print(f"  Second line: {second_line.strip()}")
print("  File is now closed:", file.closed)


# Creating a class-based context manager
print("\n3. Creating a Class-Based Context Manager:")

class Timer:
    """A context manager for timing code blocks"""
    # TODO

# Using our class-based context manager
print("\nUsing the Timer context manager:")
with Timer() as timer:
    # Simulate some work
    import time
    time.sleep(0.1)
    print("  Doing some work...")
    time.sleep(0.1)

# A more practical example: Database transaction manager
print("\nDatabase Transaction Manager Example:")

class DatabaseConnection:
    """A fake database connection for demonstration"""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False
    
    def connect(self):
        print(f"  Connecting to database: {self.connection_string}")
        self.connected = True
    
    def close(self):
        print("  Closing database connection")
        self.connected = False
    
    def execute(self, query):
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"  Executing query: {query}")
        # Simulate query execution
        return ["result1", "result2"]


class TransactionManager:
    """A context manager for database transactions"""
    
    # TODO

# Using the transaction manager
print("\nUsing the transaction manager (successful case):")
db = DatabaseConnection("postgresql://user:pass@localhost/db")
db.connect()

try:
    with TransactionManager(db) as conn:
        conn.execute("INSERT INTO users (name) VALUES ('Alice')")
        conn.execute("UPDATE accounts SET balance = 100 WHERE user_id = 1")
        print("  Transaction completed successfully")
finally:
    db.close()

# Transaction with an error
print("\nUsing the transaction manager (with error):")
db = DatabaseConnection("postgresql://user:pass@localhost/db")
db.connect()

try:
    with TransactionManager(db) as conn:
        conn.execute("INSERT INTO users (name) VALUES ('Bob')")
        # Simulate an error
        if True:
            raise ValueError("Something went wrong!")
        conn.execute("This won't be executed")
except ValueError:
    print("  Caught the error outside the with block")
finally:
    db.close()

