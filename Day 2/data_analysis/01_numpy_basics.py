# 01: NumPy Basics
print("Introduction to NumPy: The Foundation of Data Science in Python")
print("---------------------------------------------------------------")

import numpy as np
import time
import sys

# Why NumPy? Memory efficiency comparison
print("\n1. Memory Efficiency")
print("-------------------")

# Create a list and an equivalent NumPy array
python_list = list(range(1000))
numpy_array = np.array(range(1000))

# Compare memory usage
print(f"Memory size of Python list: {sys.getsizeof(python_list)} bytes")
print(f"Memory size of NumPy array: {numpy_array.nbytes} bytes")

# Performance comparison
print("\n2. Performance Comparison")
print("-----------------------")

# Function to sum all elements using a loop (Python way)
def sum_with_loop(lst):
    total = 0
    for item in lst:
        total += item
    return total

# Create larger structures for timing
size = 1000000
python_list = list(range(size))
numpy_array = np.array(range(size))

# Time Python list summation
start = time.time()
result_list = sum_with_loop(python_list)
end = time.time()
print(f"Python list sum (loop): {end - start:.6f} seconds")

# Time NumPy array summation
start = time.time()
result_numpy = np.sum(numpy_array)
end = time.time()
print(f"NumPy array sum: {end - start:.6f} seconds")

# Basic array creation
print("\n3. Creating NumPy Arrays")
print("-----------------------")

# From lists
array_1d = np.array([1, 2, 3, 4, 5])
array_2d = np.array([[1, 2, 3], [4, 5, 6]])

print(f"1D array: {array_1d}")
print(f"2D array:\n{array_2d}")

# Using built-in methods
print("\nZeros array:", np.zeros(5))
print("Ones array:", np.ones(5))
print("Identity matrix:\n", np.eye(3))
print("Range array:", np.arange(0, 10, 2))
print("Evenly spaced array:", np.linspace(0, 1, 5))
print("Random array:", np.random.random(5))

# Array properties
print("\n4. Array Properties")
print("------------------")
sample_array = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

print(f"Shape: {sample_array.shape}")
print(f"Dimensions: {sample_array.ndim}")
print(f"Size (total elements): {sample_array.size}")
print(f"Data type: {sample_array.dtype}")

# Indexing and slicing
print("\n5. Indexing and Slicing")
print("----------------------")
print(f"Original array:\n{sample_array}")
print(f"Element at position (1,2): {sample_array[1, 2]}")
print(f"First row: {sample_array[0]}")
print(f"First column: {sample_array[:, 0]}")
print(f"Sub-array (first 2 rows, last 2 columns):\n{sample_array[:2, 2:]}")

# Basic operations
print("\n6. Basic Array Operations")
print("------------------------")
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(f"a + b: {a + b}")
print(f"a * b: {a * b}")  # Element-wise multiplication
print(f"a * 2: {a * 2}")
print(f"a squared: {a ** 2}")
print(f"Sin of a: {np.sin(a)}")
print(f"Mean of a: {np.mean(a)}")
print(f"Sum of a: {np.sum(a)}")

print("\n--- Exercise ---")
print("1. Create a 3x3 matrix of random integers between 1 and 100")
print("2. Calculate the mean of each row and each column")
print("3. Find the maximum value in the entire matrix and its position")
print("4. Create a new array by normalizing the values (subtract mean and divide by std dev)")