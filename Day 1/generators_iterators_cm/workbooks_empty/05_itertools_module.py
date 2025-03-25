# 05: The itertools Module
print("The itertools Module")
print("------------------")

import itertools 
import time
import operator
from functools import reduce


# count - counting from a starting value
print("\ncount(start, [step]) - Count from start by step")


# cycle - cycle through an iterable indefinitely
print("\ncycle(iterable) - Cycle through elements repeatedly")


# repeat - repeat a value indefinitely or a specific number of times
print("\nrepeat(elem, [n]) - Repeat an element n times or indefinitely")


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

# takewhile - take items while predicate is true
print("\ntakewhile(predicate, iterable) - Take items while predicate is true")

# filterfalse - filter elements where predicate is false
print("\nfilterfalse(predicate, iterable) - Filter items where predicate is false")


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

# TODO

print(f"Data: {data}")
print("Running averages:", end=" ")
for count, avg in running_averages:
    print(f"({avg:.2f})", end=" ")
print()

# Example 2: Sliding window with islice and tee
print("\nSliding window implementation:")

# TODO



"""\n--- Exercise ---
1. Implement a 'round-robin' scheduler using itertools functions.
2. Create a function to find the most common N-grams (letter sequences) in a text."""


