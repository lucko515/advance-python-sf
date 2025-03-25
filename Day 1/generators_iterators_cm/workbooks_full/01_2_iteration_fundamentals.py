# Creating a simple iterator class
print("\nCreating a simple iterator:")

class CountDown:
    """Iterator that counts down from n to 1"""
    
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        # Return an iterator (self)
        return self
    
    def __next__(self):
        if self.start <= 0:
            # Signal the end of iteration
            raise StopIteration
        
        self.start -= 1
        return self.start + 1

# Using our custom iterator
countdown = CountDown(3)
print("Custom iterator countdown from 3:")
for num in countdown:
    print(f"  {num}")

# Try to use it again
print("Trying to use the iterator again:")
for num in countdown:
    print(f"  {num}")  # Nothing will print, iterator is exhausted

"""\n--- Exercise ---
1. Create a simple Range iterator class that mimics the built-in range()
   function but returns squares of numbers instead of the numbers themselves.
2. Create an EvenNumbers iterator class that returns only even numbers up to a limit."""

