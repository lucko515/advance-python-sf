# 06: Context Managers
print("Context Managers")
print("---------------")


# Traditional approach vs. with statement
print("\n1. Traditional vs. With Statement:")


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
    
    def __enter__(self):
        """Enter the context, start the timer"""
        import time
        self.start_time = time.time()
        return self  # The as variable will be assigned this value
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context, stop the timer and print duration"""
        import time
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print(f"  Time taken: {self.duration:.6f} seconds")
        # Returning False (or None) will propagate exceptions
        # Returning True would suppress exceptions
        return False

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
    
    def __init__(self, connection):
        self.connection = connection
    
    def __enter__(self):
        print("  Beginning transaction")
        self.connection.execute("BEGIN TRANSACTION")
        return self.connection  # Return the connection for use in the with block
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # An exception occurred, rollback the transaction
            print(f"  Error occurred: {exc_val}")
            print("  Rolling back transaction")
            self.connection.execute("ROLLBACK")
        else:
            # No exception, commit the transaction
            print("  Committing transaction")
            self.connection.execute("COMMIT")
        return False  # Propagate exceptions

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

