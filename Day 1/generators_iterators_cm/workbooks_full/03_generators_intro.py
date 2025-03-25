# 03: Generators Introduction
print("Generators: Introduction")
print("-----------------------")

# The problem: implementing iterators requires a lot of boilerplate

def count_to(n):
    """Generator that counts from 1 to n"""
    current = 1
    while current <= n:
        yield current
        current += 1

# Using our generator
print("\nUsing a generator function:")
counter = count_to(5)
print(f"Generator object: {counter}")
print(f"Type: {type(counter)}")

# Manual iteration
print("\nManual iteration:")
print(f"  {next(counter)}")  # 1
print(f"  {next(counter)}")  # 2
print(f"  {next(counter)}")  # 3
print(f"  {next(counter)}")  # 4
print(f"  {next(counter)}")  # 5

try:
    print(f"  {next(counter)}")  # StopIteration exception
except StopIteration:
    print("  No more items!")

# In a for loop (create a new generator)
print("\nIn a loop:")
for num in count_to(5):
    print(f"  {num}", end=" ")
print()

# How generators maintain state
print("\nHow generators maintain state:")

def fibonacci(limit):
    """Generate Fibonacci numbers up to a limit"""
    a, b = 0, 1
    count = 0
    
    while count < limit:
        print(f"  [Generator state: a={a}, b={b}, count={count}]")
        yield a
        a, b = b, a + b
        count += 1

print("\nGenerating Fibonacci numbers with state tracking:")
for num in fibonacci(6):
    print(f"  Yielded: {num}")

# Generator expressions (like list comprehensions but lazy)
print("\nGenerator Expressions:")

# List comprehension - evaluates immediately
numbers = [1, 2, 3, 4, 5]
squares_list = [x**2 for x in numbers]
print(f"List comprehension: {squares_list}")
print(f"Type: {type(squares_list)}")

# Generator expression - evaluates lazily
squares_gen = (x**2 for x in numbers)
print(f"Generator expression: {squares_gen}")
print(f"Type: {type(squares_gen)}")

print("\nConsuming generator expression:")
for square in squares_gen:
    print(f"  {square}", end=" ")
print()

# Memory efficiency comparison
print("\nMemory Efficiency:")

def first_n_squares(n):
    """Generate squares of numbers from 0 to n-1"""
    for i in range(n):
        yield i**2

# Using a generator for large sequences
n = 10_000_000  # 10 million

print(f"Creating a list of {n:,} squares would use a lot of memory")
print("Using a generator instead:")
squares = first_n_squares(n)
print(f"First 5 squares from generator: ", end="")
count = 0
for square in squares:
    if count < 5:
        print(square, end=" ")
        count += 1
    else:
        print("... (and so on)")
        break

# Pipeline of generators
print("\nBuilding a pipeline of generators:")

def integers():
    """Generate the integers 1, 2, 3, ..."""
    i = 1
    while True:
        yield i
        i += 1

def squared(seq):
    """Yield the squared values from seq."""
    for i in seq:
        yield i * i

def take(n, seq):
    """Take the first n values from seq."""
    for i, val in enumerate(seq):
        if i >= n:
            break
        yield val

# Create a pipeline
pipeline = take(5, squared(integers()))

print("First 5 squared integers:")
for num in pipeline:
    print(f"  {num}", end=" ")
print()

# Reading a large file with generators
print("\nReading large files with generators:")

def read_large_file(file_path, chunk_size=1024):
    """Lazy function to read a large file piece by piece."""
    # Note: We're simulating this for the example
    print(f"  [Opening file: {file_path}]")
    print(f"  [Reading in chunks of {chunk_size} bytes]")
    
    # Simulate reading chunks
    chunks = ["Chunk 1: Data...", "Chunk 2: More data...", "Chunk 3: Final data..."]
    for chunk in chunks:
        print(f"  [Yielding chunk]")
        yield chunk
    
    print(f"  [File closed]")

# Process a simulated large file
print("Processing a large log file:")
chunks = read_large_file("huge_log.txt")

for i, chunk in enumerate(chunks, 1):
    print(f"  Processing {i}: {chunk}")

"""\n--- Exercise ---
1. Create a generator function that produces a sequence of prime numbers.
2. Implement the Fibonacci sequence as a generator expression (if possible)."""
