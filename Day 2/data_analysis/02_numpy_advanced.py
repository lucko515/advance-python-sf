# 02: Advanced NumPy Features
print("Advanced NumPy: Broadcasting and Vectorization")
print("----------------------------------------------")

import numpy as np
import time
import matplotlib.pyplot as plt

# Brief review from previous session
print("\n1. Quick Review")
print("-------------")
array_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"2D array:\n{array_2d}")
print(f"Shape: {array_2d.shape}")
print(f"Sum of all elements: {np.sum(array_2d)}")

# Broadcasting
print("\n2. Broadcasting")
print("--------------")
print("Broadcasting allows NumPy to perform operations on arrays of different shapes")

# Example 1: Adding a scalar to an array
a = np.array([1, 2, 3])
print(f"Array: {a}")
print(f"Array + 10: {a + 10}")  # 10 is broadcast to [10, 10, 10]

# Example 2: Operations between arrays of different dimensions
print("\nBroadcasting between different dimensions:")
row = np.array([1, 2, 3])  # Shape: (3,)
column = np.array([[10], [20], [30]])  # Shape: (3, 1)
print(f"Row vector: {row}")
print(f"Column vector:\n{column}")
print(f"Result of row + column:\n{row + column}")  
# Explanation: row is broadcast to [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
# column is broadcast to [[10, 10, 10], [20, 20, 20], [30, 30, 30]]
# Then addition happens element-wise

# Example 3: Broadcasting rules visualization
print("\nBroadcasting rules visualization:")
print("Smaller arrays are 'stretched' to match the shape of larger arrays")
print("Arrays must be compatible: dimensions must be equal or one must be 1")

# Create matrices for temperature data example
days = 5
cities = 3
temperatures = np.random.randint(60, 100, size=(days, cities))
print(f"\nTemperatures for {cities} cities over {days} days:\n{temperatures}")

# City averages (across days)
city_avg = np.mean(temperatures, axis=0)
print(f"Average temperature per city: {city_avg}")

# Temperature difference from city average (broadcasting in action)
# Broadcasting the city averages to match the original array shape
temp_diffs = temperatures - city_avg  # Broadcasts city_avg to match temperatures shape
print(f"Temperature differences from city averages:\n{temp_diffs}")

# Vectorization vs. loops
print("\n3. Vectorization")
print("--------------")
print("Vectorization means operating on entire arrays without explicit loops")

# Create a large array for demonstration
size = 1_000_000
large_array = np.random.random(size)

# Calculate square root using a loop
def sqrt_loop(arr):
    result = np.zeros_like(arr)
    for i in range(len(arr)):
        result[i] = arr[i] ** 0.5
    return result

# Time the loop version
start = time.time()
result_loop = sqrt_loop(large_array)
loop_time = time.time() - start
print(f"Loop time: {loop_time:.6f} seconds")

# Calculate using vectorized NumPy
start = time.time()
result_vectorized = np.sqrt(large_array)
vectorized_time = time.time() - start
print(f"Vectorized time: {vectorized_time:.6f} seconds")
print(f"Speedup: {loop_time / vectorized_time:.1f}x faster")

# Advanced array manipulation
print("\n4. Array Reshaping and Manipulation")
print("---------------------------------")

# Reshaping arrays
original = np.arange(12)
print(f"Original array: {original}")
reshaped = original.reshape(3, 4)
print(f"Reshaped to 3x4:\n{reshaped}")
reshaped_again = original.reshape(4, 3)
print(f"Reshaped to 4x3:\n{reshaped_again}")

# Transposing
print(f"\nTransposed array:\n{reshaped.T}")

# Stacking arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(f"\nVertical stack:\n{np.vstack((a, b))}")
print(f"Horizontal stack:\n{np.hstack((a, b))}")

# Splitting arrays
big_array = np.arange(16).reshape(4, 4)
print(f"\nOriginal big array:\n{big_array}")
split_arrays = np.split(big_array, 2, axis=0)
print(f"Split into 2 horizontally:\n{split_arrays[0]}\n{split_arrays[1]}")

# Universal Functions (ufuncs)
print("\n5. Universal Functions (ufuncs)")
print("------------------------------")
print("ufuncs operate element-wise on arrays and are optimized for performance")

data = np.linspace(0, 2*np.pi, 10)
print(f"Data points: {data}")
print(f"Sine: {np.sin(data)}")
print(f"Cosine: {np.cos(data)}")
print(f"Exponent: {np.exp(data)}")

# Multiple operations chained (still vectorized)
result = np.sin(data) * np.cos(data) + np.exp(-data)
print(f"Complex expression result: {result}")

# Application: Image processing example (simplified)
print("\n6. Simple Application: Image Processing")
print("-------------------------------------")

# Create a simple "image" (grayscale)
image = np.zeros((5, 5))
image[1:4, 1:4] = 1  # Add a white square
print("Original image:")
print(image)

# Apply a simple filter (blur) using convolution
kernel = np.ones((3, 3)) / 9  # Simple averaging filter
print("\nKernel (filter):")
print(kernel)

# Manually apply the filter (simplified convolution)
# In real applications, you'd use scipy.signal.convolve2d
filtered_image = np.zeros_like(image)
for i in range(1, image.shape[0]-1):
    for j in range(1, image.shape[1]-1):
        filtered_image[i, j] = np.sum(image[i-1:i+2, j-1:j+2] * kernel)

print("\nFiltered image (blurred):")
print(filtered_image)

print("\n--- Exercise ---")
print("1. Create a temperature dataset for 7 days across 5 cities")
print("2. Calculate the daily average temperature across all cities")
print("3. Find which cities were above or below the daily average")
print("4. Calculate how much each city deviates from its own weekly average")