# 02: Advanced Iterator Patterns
print("Advanced Iterator Patterns")
print("-------------------------")

# Separating iterable and iterator (better practice)
print("Separating iterable and iterator:")

class FibonacciNumbers:
    """An iterable that produces Fibonacci sequence"""
    
    def __init__(self, limit):
        self.limit = limit
    
    def __iter__(self):
        # Return a new iterator each time
        return FibonacciIterator(self.limit)


class FibonacciIterator:
    """Iterator that produces Fibonacci numbers up to a limit"""
    
    def __init__(self, limit):
        self.limit = limit
        self.previous = 0
        self.current = 1
        self.count = 0
    
    def __iter__(self):
        # An iterator must also be iterable (return self)
        return self
    
    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration
        
        if self.count == 0:
            self.count += 1
            return 0
        elif self.count == 1:
            self.count += 1
            return 1
        else:
            result = self.previous + self.current
            self.previous, self.current = self.current, result
            self.count += 1
            return result

# Using our well-designed iterable
print("\nFibonacci sequence (limit 8):")
fib = FibonacciNumbers(8)
for num in fib:
    print(f"  {num}", end=" ")
print()

# We can reuse the iterable to get a fresh sequence
print("\nReusing the iterable (fresh iterator):")
for num in fib:
    print(f"  {num}", end=" ")
print()

# Implementing an infinite iterator (with safeguards)
print("\nInfinite Iterators (with safeguards):")

class InfiniteCounter:
    """An infinite counter that yields 0, 1, 2, ... forever"""
    
    def __init__(self, start=0):
        self.start = start
    
    def __iter__(self):
        return InfiniteCounterIterator(self.start)


class InfiniteCounterIterator:
    """Iterator for InfiniteCounter with a safety limit"""
    
    def __init__(self, start):
        self.current = start
        # Safety to prevent infinite loops
        self.max_iterations = 1000000  # A very large number
        self.iterations = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.iterations >= self.max_iterations:
            raise RuntimeError("Potential infinite loop detected")
        
        result = self.current
        self.current += 1
        self.iterations += 1
        return result

# Using our infinite counter (but limiting output)
counter = InfiniteCounter()
counter_iter = iter(counter)

print("First 5 values from the infinite counter:")
for _ in range(5):
    print(f"  {next(counter_iter)}", end=" ")
print()

# Implementing a practical iterator: Chunking
print("\nPractical Iterator: Chunking Data")

class Chunker:
    """Split an iterable into chunks of specified size"""
    
    def __init__(self, iterable, chunk_size):
        self.iterable = iterable
        self.chunk_size = chunk_size
    
    def __iter__(self):
        return ChunkerIterator(self.iterable, self.chunk_size)


class ChunkerIterator:
    """Iterator that yields chunks from the source iterable"""
    
    def __init__(self, iterable, chunk_size):
        self.iterator = iter(iterable)
        self.chunk_size = chunk_size
    
    def __iter__(self):
        return self
    
    def __next__(self):
        chunk = []
        try:
            for _ in range(self.chunk_size):
                chunk.append(next(self.iterator))
        except StopIteration:
            if not chunk:  # If we didn't add any items before exception
                raise
        return chunk

# Using the chunker
data = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Original data: {data}")

chunker = Chunker(data, 3)
print("Data in chunks of 3:")
for chunk in chunker:
    print(f"  {chunk}")

# The takewhile pattern - another useful iterator pattern
print("\nTakewhile Pattern:")

class TakeWhile:
    """Iterator that takes values while a condition is true"""
    
    def __init__(self, iterable, condition):
        self.iterable = iterable
        self.condition = condition
    
    def __iter__(self):
        return TakeWhileIterator(self.iterable, self.condition)


class TakeWhileIterator:
    """Iterator for TakeWhile"""
    
    def __init__(self, iterable, condition):
        self.iterator = iter(iterable)
        self.condition = condition
        self.done = False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.done:
            raise StopIteration
        
        value = next(self.iterator)
        if self.condition(value):
            return value
        else:
            self.done = True
            raise StopIteration

# Using TakeWhile
numbers = [2, 4, 6, 7, 8, 10, 12]
print(f"Original numbers: {numbers}")

# Take values while they're even
take_while_even = TakeWhile(numbers, lambda x: x % 2 == 0)
print("Numbers while even:")
for num in take_while_even:
    print(f"  {num}", end=" ")
print()

# Combining iterator patterns
print("\nCombining Iterator Patterns:")

def is_less_than_ten(x):
    return x < 10

infinite = InfiniteCounter(1)  # Starts at 1 and counts up
squared = map(lambda x: x**2, infinite)  # Square each number
filtered = TakeWhile(squared, is_less_than_ten)  # Take until we hit 10 or more

print("Squares of numbers less than 10:")
for num in filtered:
    print(f"  {num}", end=" ")
print()

"""\n--- Exercise ---
1. Create a PeekableIterator class that wraps another iterator and allows
    'peeking' at the next value without consuming it."""

