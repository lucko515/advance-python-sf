# 05: Profiling and Optimizing Python Code
print("Profiling and Optimizing Python Code")
print("---------------------------------")

import time
import timeit
import random
import functools
import sys
from collections import Counter

# 1. Basic Timing with time.time()
print("\n1. Basic Timing with time.time()")
print("------------------------------")

def measure_time(func, *args, **kwargs):
    """Measure the execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"{func.__name__} took {end_time - start_time:.6f} seconds to run")
    return result

# Example function to time
def slow_sum(n):
    """Sum numbers from 0 to n-1 slowly."""
    total = 0
    for i in range(n):
        total += i
    return total

def fast_sum(n):
    """Sum numbers from 0 to n-1 using a mathematical formula."""
    return (n * (n - 1)) // 2

# Measure and compare
n = 1000000
measure_time(slow_sum, n)
measure_time(fast_sum, n)

# 2. Using timeit for more precise timing
print("\n2. Using timeit for more precise timing")
print("-----------------------------------")

def time_function(func_str, setup_str, number=1000):
    """Time a function using timeit."""
    time_taken = timeit.timeit(func_str, setup=setup_str, number=number)
    print(f"{func_str} took {time_taken/number:.6f} seconds per run (averaged over {number} runs)")
    return time_taken

# Time different list creation methods
list_comp_time = time_function(
    "[i for i in range(100)]",
    "import random",
)

map_time = time_function(
    "list(map(lambda x: x, range(100)))",
    "import random",
)

for_loop_time = time_function(
    "result = []; [result.append(i) for i in range(100)]",
    "import random",
)

print("\nUsing timeit for function comparisons:")

# Define functions to compare
def list_comprehension():
    return [i*i for i in range(1000)]

def map_function():
    return list(map(lambda x: x*x, range(1000)))

def for_loop():
    result = []
    for i in range(1000):
        result.append(i*i)
    return result

# Time them with timeit
print("\nComparing different ways to square numbers 0-999:")
for func in [list_comprehension, map_function, for_loop]:
    timer = timeit.Timer(functools.partial(func))
    print(f"{func.__name__}: {timer.timeit(number=100)/100:.6f} seconds per run")

# 3. Profiling with cProfile
print("\n3. Profiling with cProfile")
print("------------------------")
print("In a real scenario, you'd run: python -m cProfile -s cumtime your_script.py")
print("Here's a sample of what would be shown:\n")

# Define a sample program to profile
def sample_program():
    data = generate_data(10000)
    result1 = process_data_slow(data)
    result2 = process_data_fast(data)
    return result1, result2

def generate_data(size):
    return [random.randint(0, 100) for _ in range(size)]

def process_data_slow(data):
    result = []
    for item in data:
        result.append(fibonacci_recursive(item % 20))
    return result

def process_data_fast(data):
    return [fibonacci_memo(item % 20) for item in data]

def fibonacci_recursive(n):
    """Calculate Fibonacci number recursively (inefficient)."""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

@functools.lru_cache(maxsize=None)
def fibonacci_memo(n):
    """Calculate Fibonacci number with memoization."""
    if n <= 1:
        return n
    return fibonacci_memo(n-1) + fibonacci_memo(n-2)

print("\ncProfile example output (simplified):")
print("   ncalls  tottime  percall  cumtime  percall filename:lineno(function)")
print("     10000    0.002    0.000    0.002    0.000 profiling.py:generate_data")
print("         1    0.001    0.001    8.753    8.753 profiling.py:process_data_slow")
print("     10000    8.750    0.001    8.750    0.001 profiling.py:fibonacci_recursive")
print("         1    0.003    0.003    0.005    0.005 profiling.py:process_data_fast")
print("     10000    0.001    0.000    0.001    0.000 profiling.py:fibonacci_memo")

print("\nTo use cProfile in your own code:")
print("import cProfile")
print("cProfile.run('your_function()')")

# Demonstrate how to use cProfile programmatically
import cProfile
import io
import pstats

def profile_func(func, *args, **kwargs):
    """Profile a function and print results."""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()
    
    # Print stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(10)  # Print top 10 lines
    print(s.getvalue())
    
    return result

# Small version for demo purposes
def mini_sample():
    data = generate_data(100)
    result = process_data_slow(data)
    return result

print("\nActual cProfile output for a small example:")
result = profile_func(mini_sample)

# 4. Common Performance Bottlenecks
print("\n4. Common Performance Bottlenecks")
print("------------------------------")

print("\n4.1 Inefficient Data Structures")
print("----------------------------")

def find_item_in_list(item, items):
    """Find an item in a list (O(n) operation)."""
    return item in items

def find_item_in_set(item, items):
    """Find an item in a set (O(1) operation)."""
    return item in items

# Create test data
test_range = 10000
test_list = list(range(test_range))
test_set = set(test_list)
lookup_item = test_range - 1  # Worst case for list

# Compare performance
print("\nLooking up the last item in a collection of 10,000 items:")
list_time = timeit.timeit(lambda: find_item_in_list(lookup_item, test_list), number=1000)
set_time = timeit.timeit(lambda: find_item_in_set(lookup_item, test_set), number=1000)

print(f"List lookup: {list_time:.6f} seconds (for 1000 lookups)")
print(f"Set lookup:  {set_time:.6f} seconds (for 1000 lookups)")
print(f"Set is {list_time/set_time:.1f}x faster")

print("\n4.2 String Concatenation in Loops")
print("------------------------------")

def build_string_concat(n):
    """Build a string by concatenation in a loop."""
    result = ""
    for i in range(n):
        result += str(i)
    return result

def build_string_join(n):
    """Build a string using a list and join."""
    result = []
    for i in range(n):
        result.append(str(i))
    return "".join(result)

n_items = 10000
print(f"\nBuilding a string from {n_items} numbers:")
concat_time = timeit.timeit(lambda: build_string_concat(n_items), number=5)
join_time = timeit.timeit(lambda: build_string_join(n_items), number=5)

print(f"Concatenation: {concat_time:.6f} seconds (for 5 runs)")
print(f"Join method:   {join_time:.6f} seconds (for 5 runs)")
print(f"Join is {concat_time/join_time:.1f}x faster")

print("\n4.3 Function Call Overhead")
print("-----------------------")

def calculate_with_functions(n):
    """Calculate sum of squares using separate function calls."""
    def square(x):
        return x * x
    
    total = 0
    for i in range(n):
        total += square(i)
    return total

def calculate_inline(n):
    """Calculate sum of squares with inline calculation."""
    total = 0
    for i in range(n):
        total += i * i
    return total

n_items = 1000000
print(f"\nCalculating sum of squares for {n_items} numbers:")
functions_time = timeit.timeit(lambda: calculate_with_functions(n_items), number=3)
inline_time = timeit.timeit(lambda: calculate_inline(n_items), number=3)

print(f"With function calls: {functions_time:.6f} seconds (for 3 runs)")
print(f"With inline code:    {inline_time:.6f} seconds (for 3 runs)")
print(f"Inline is {functions_time/inline_time:.1f}x faster")

# 5. Memory Profiling
print("\n5. Memory Profiling")
print("-----------------")

def demonstrate_memory_usage():
    """Demonstrate memory usage patterns."""
    print("\nMemory usage examples:")
    
    # Example 1: Creating a large list
    large_list = [0] * 1000000
    print(f"Large list size: {sys.getsizeof(large_list)} bytes")
    
    # Example 2: String operations
    original = "a" * 1000000
    doubled = original + original
    print(f"Original string size: {sys.getsizeof(original)} bytes")
    print(f"Doubled string size: {sys.getsizeof(doubled)} bytes")
    
    # Example 3: Dictionary vs List for counting
    data = ["apple", "banana", "cherry", "apple", "banana", "apple"] * 100000
    
    # Using a dictionary for counting
    counter_dict = {}
    for item in data:
        if item in counter_dict:
            counter_dict[item] += 1
        else:
            counter_dict[item] = 1
    
    # Using Counter from collections
    counter = Counter(data)
    
    print(f"Dictionary counter size: {sys.getsizeof(counter_dict)} bytes")
    print(f"Collections.Counter size: {sys.getsizeof(counter)} bytes")
    
    # Clean up to free memory
    del large_list, original, doubled, data, counter_dict, counter

# Only run if you have enough memory
demonstrate_memory_usage()

# 6. Optimization Strategies
print("\n6. Optimization Strategies")
print("-----------------------")
