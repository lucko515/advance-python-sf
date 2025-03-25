# 05: The itertools Module
print("The itertools Module")
print("------------------")

import itertools 
import time
import operator
from functools import reduce



# count - counting from a starting value
print("\ncount(start, [step]) - Count from start by step")
counter = itertools.count(10, 2)
print("itertools.count(10, 2):", end=" ")
for _ in range(5):
    print(next(counter), end=" ")
print()

# cycle - cycle through an iterable indefinitely
print("\ncycle(iterable) - Cycle through elements repeatedly")
cycler = itertools.cycle(["red", "green", "blue"])
print("itertools.cycle(['red', 'green', 'blue']):", end=" ")
for _ in range(7):
    print(next(cycler), end=" ")
print()

# repeat - repeat a value indefinitely or a specific number of times
print("\nrepeat(elem, [n]) - Repeat an element n times or indefinitely")
repeater = itertools.repeat("Hello", 3)
print("itertools.repeat('Hello', 3):", end=" ")
for item in repeater:
    print(item, end=" ")
print()

# Terminating Iterators
print("\n2. Terminating Iterators:")

# chain - chain multiple iterables together
print("\nchain(*iterables) - Chain multiple iterables into a single sequence")
result = itertools.chain([1, 2], [3, 4, 5], [6])
print("itertools.chain([1, 2], [3, 4, 5], [6]):", list(result))

# compress - filter elements based on selectors
print("\ncompress(data, selectors) - Filter one iterable with another")
result = itertools.compress("ABCDEF", [1, 0, 1, 0, 1, 1])
print("itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1]):", "".join(result))

# dropwhile - drop items while predicate is true
print("\ndropwhile(predicate, iterable) - Drop items while predicate is true")
result = itertools.dropwhile(lambda x: x < 5, [1, 3, 6, 2, 1, 9, 8])
print("itertools.dropwhile(lambda x: x < 5, [1, 3, 6, 2, 1, 9, 8]):", list(result))

# takewhile - take items while predicate is true
print("\ntakewhile(predicate, iterable) - Take items while predicate is true")
result = itertools.takewhile(lambda x: x < 5, [1, 3, 6, 2, 1, 9, 8])
print("itertools.takewhile(lambda x: x < 5, [1, 3, 6, 2, 1, 9, 8]):", list(result))

# filterfalse - filter elements where predicate is false
print("\nfilterfalse(predicate, iterable) - Filter items where predicate is false")
result = itertools.filterfalse(lambda x: x % 2 == 0, range(10))
print("itertools.filterfalse(lambda x: x % 2 == 0, range(10)):", list(result))

# groupby - group consecutive items by a key function
print("\ngroupby(iterable, key=None) - Group consecutive items")
data = "AAAABBBCCDAABB"
groups = []
for key, group in itertools.groupby(data):
    groups.append((key, list(group)))
print("itertools.groupby('AAAABBBCCDAABB'):", groups)

# Sorted first for efficient groupby
data = "AAAABBBCCDAABB"
sorted_data = ''.join(sorted(data))
groups = []
for key, group in itertools.groupby(sorted_data):
    groups.append((key, list(group)))
print("itertools.groupby(''.join(sorted('AAAABBBCCDAABB'))):", groups)

# islice - slice an iterator
print("\nislice(iterable, start, stop, step) - Slice an iterator")
result = itertools.islice("ABCDEFGH", 2, 6, 2)
print("itertools.islice('ABCDEFGH', 2, 6, 2):", "".join(result))

# zip_longest - zip iterables, filling missing values
print("\nzip_longest(*iterables, fillvalue=None) - Zip with longest iterable")
result = itertools.zip_longest("ABCD", "xy", fillvalue="-")
print("itertools.zip_longest('ABCD', 'xy', fillvalue='-'):", list(result))

# Combinatoric Generators
print("\n3. Combinatoric Generators:")

# product - cartesian product of input iterables
print("\nproduct(*iterables, repeat=1) - Cartesian product")
result = itertools.product("AB", "12")
print("itertools.product('AB', '12'):", list(result))

# permutations - all possible orderings
print("\npermutations(iterable, r=None) - All possible orderings")
result = itertools.permutations("ABC", 2)
print("itertools.permutations('ABC', 2):", list(result))

# combinations - r-length combinations
print("\ncombinations(iterable, r) - r-length combinations")
result = itertools.combinations("ABCD", 2)
print("itertools.combinations('ABCD', 2):", list(result))

# combinations_with_replacement - combinations with repeats
print("\ncombinations_with_replacement(iterable, r) - Combinations with repetition")
result = itertools.combinations_with_replacement("ABC", 2)
print("itertools.combinations_with_replacement('ABC', 2):", list(result))

# Practical Examples
print("\n4. Practical Examples:")

# Example 1: Running average calculator using accumulate
print("\nRunning average calculator:")
data = [3, 4, 6, 2, 8, 9, 3]

def running_avg(prev_avg, item, count=None):
    """Calculate the running average"""
    # items is a tuple containing (running_count, running_avg)
    count, avg = prev_avg
    count += 1
    avg = avg + (item - avg) / count
    return (count, avg)

# Initialize with (count, average)
running_averages = itertools.accumulate(data, lambda acc, x: (acc[0] + 1, acc[1] + (x - acc[1]) / (acc[0] + 1)), initial=(0, 0))

print(f"Data: {data}")
print("Running averages:", end=" ")
for count, avg in running_averages:
    print(f"({avg:.2f})", end=" ")
print()

# Example 2: Sliding window with islice and tee
print("\nSliding window implementation:")

def sliding_window(iterable, n):
    """Create a sliding window of size n over iterable"""
    iterables = itertools.tee(iterable, n)
    
    for i, it in enumerate(iterables):
        # Advance iterators to create staggered starts
        for _ in range(i):
            next(it, None)
            
    # Zip them up and return
    return zip(*iterables)

text = "ABCDEFGHIJ"
windows = sliding_window(text, 3)
print(f"Sliding windows of size 3 over '{text}':")
for window in windows:
    print(f"  {''.join(window)}")



"""\n--- Exercise ---
1. Implement a 'round-robin' scheduler using itertools functions.
2. Create a function to find the most common N-grams (letter sequences) in a text."""


