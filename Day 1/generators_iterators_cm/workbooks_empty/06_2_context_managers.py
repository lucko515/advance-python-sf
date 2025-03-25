import os
import contextlib

@contextlib.contextmanager
def file_manager(filename, mode):
    """A simple file manager using contextlib"""
    try:
        # Setup - acquire resource
        file = open(filename, mode)
        print(f"  Opened file: {filename} in mode {mode}")
        # Yield the resource
        yield file
    finally:
        # Teardown - release resource
        file.close()
        print(f"  Closed file: {filename}")

# Using the generator-based context manager
print("\nUsing the generator-based file manager:")
with file_manager("example.txt", "r") as file:
    lines = file.readlines()
    print(f"  Read {len(lines)} lines from the file")

# Another example: temporarily changing a working directory


@contextlib.contextmanager
def working_directory(path):
    """Temporarily change working directory"""
    # Setup
    current_dir = os.getcwd()
    print(f"  Current directory: {current_dir}")
    print(f"  Changing to: {path}")
    # In a real implementation, we would actually change directories
    # os.chdir(path)
    
    try:
        yield
    finally:
        # Cleanup
        print(f"  Changing back to: {current_dir}")
        # os.chdir(current_dir)

# Using the working directory context manager
print("\nUsing the working directory context manager:")
with working_directory("/tmp"):
    print("  Doing work in temporary directory")
    # In a real implementation, files would be created in /tmp

# Error handling in context managers
print("\n5. Error Handling in Context Managers:")

@contextlib.contextmanager
def error_handler(operation_name):
    """A context manager that handles errors and logs them"""
    print(f"  Starting operation: {operation_name}")
    try:
        yield
        print(f"  Operation completed successfully: {operation_name}")
    except Exception as e:
        print(f"  Error during operation '{operation_name}': {e}")
        # We can choose to suppress the exception by not re-raising it
        # Or we can re-raise it to propagate it
        # raise

# Using the error handler to suppress exceptions
print("\nUsing the error handler (suppressing exceptions):")
with error_handler("data processing"):
    # Simulate an error
    raise ValueError("Invalid data format")
print("  Code execution continues here if exception is suppressed")

# Combining multiple context managers
print("\n6. Combining Multiple Context Managers:")

# Nested with statements
print("\nNested with statements:")
with open("example.txt", "r") as file:
    with Timer() as timer:
        content = file.read()
        print(f"  Read {len(content)} characters")

# Multiple context managers in a single with statement
print("\nMultiple context managers in a single with statement:")
with open("example.txt", "r") as file, Timer() as timer:
    content = file.read()
    print(f"  Read {len(content)} characters")

# Using ExitStack for dynamic context manager composition
print("\n7. Dynamic Composition with ExitStack:")

@contextlib.contextmanager
def logger(name):
    """A simple logger context manager"""
    print(f"  Logger {name} started")
    try:
        yield
    finally:
        print(f"  Logger {name} finished")

# Using ExitStack to dynamically handle multiple context managers
print("\nUsing ExitStack for dynamic context management:")
with contextlib.ExitStack() as stack:
    # Add context managers to the stack
    file = stack.enter_context(open("example.txt", "r"))
    stack.enter_context(Timer())
    stack.enter_context(logger("main"))
    stack.enter_context(logger("secondary"))
    
    # Use the resources
    content = file.read()
    print(f"  Read {len(content)} characters")

# Practical patterns and recipes
print("\n8. Practical Patterns and Recipes:")

# Context manager for temporarily modifying an object's attributes
@contextlib.contextmanager
def temp_attributes(obj, **kwargs):
    """Temporarily set attributes on an object"""
    # Save original attributes
    original_values = {}
    for key, value in kwargs.items():
        if hasattr(obj, key):
            original_values[key] = getattr(obj, key)
        setattr(obj, key, value)
    
    try:
        yield obj
    finally:
        # Restore original attributes
        for key in kwargs:
            if key in original_values:
                setattr(obj, key, original_values[key])
            else:
                delattr(obj, key)


# Clean-up context manager to remove files
print("\nClean-up context manager:")

@contextlib.contextmanager
def temporary_file(filename, content=None):
    """Create a temporary file that gets deleted afterward"""
    try:
        with open(filename, 'w') as f:
            if content:
                f.write(content)
        print(f"  Created temporary file: {filename}")
        yield filename
    finally:
        import os
        if os.path.exists(filename):
            os.remove(filename)
            print(f"  Removed temporary file: {filename}")

# Using the temporary file context manager
print("\nUsing a self-cleaning temporary file:")
with temporary_file("temp_config.txt", content="key=value\nmode=test") as filename:
    with open(filename, 'r') as f:
        content = f.read()
    print(f"  Read from temporary file: {content.strip()}")

print("  File should be deleted now")


"""\n--- Exercise ---
1. Create a context manager that suppresses specific exceptions."""
