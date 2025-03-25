# 01: Iteration Fundamentals
print("Python Iteration Fundamentals")
print("----------------------------")

# Basic iteration we're all familiar with
print("Basic list iteration:")
fruits = ["apple", "banana", "cherry"]


# Important distinction: Iterables vs. Iterators
#  Iterables vs. Iterators

# Demonstrating iterables vs iterators
my_list = [1, 2, 3]
print(f"\nIs my_list iterable? {'__iter__' in dir(my_list)}")
print(f"Is my_list an iterator? {'__next__' in dir(my_list)}")

list_iterator = iter(my_list)
print(f"Is list_iterator iterable? {'__iter__' in dir(list_iterator)}")
print(f"Is list_iterator an iterator? {'__next__' in dir(list_iterator)}")


# String iteration
word = "Python"
print("String iteration:")
for char in word:
    print(f"  {char}")

# Dictionary iteration
user = {"name": "Alice", "age": 30, "role": "Developer"}
print("\nDictionary iteration (keys by default):")
for key in user:
    print(f"  {key}: {user[key]}")

print("\nDictionary items:")
for key, value in user.items():
    print(f"  {key}: {value}")

# Multiple iteration
print("\nIterables can be iterated multiple times:")
numbers = [1, 2, 3]
print("First iteration:")
for n in numbers:
    print(f"  {n}")
print("Second iteration:")
for n in numbers:
    print(f"  {n}")

# But iterators are exhausted after one use
print("\nIterators are exhausted after one use:")
numbers_iter = iter(numbers)
print("First iteration of the iterator:")
for n in numbers_iter:
    print(f"  {n}")
print("Second iteration of the same iterator:")
for n in numbers_iter:
    print(f"  {n}")  # Nothing will print, iterator is exhausted
