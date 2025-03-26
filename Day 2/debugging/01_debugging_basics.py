# 01: Debugging Basics
print("Python Debugging Fundamentals")
print("----------------------------")

# Let's start with a simple function that has a bug
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# This will raise a ZeroDivisionError if the list is empty
try:
    result = calculate_average([])
    print(f"The average is: {result}")
except ZeroDivisionError as e:
    print(f"Error: {e}")
    print("Cannot calculate the average of an empty list")

print("\n1. Print-based debugging (the common but limited approach)")
print("-----------------------------------------------------------")

def find_largest(numbers):
    if not numbers:
        return None
    
    # Debugging with print statements - inefficient approach
    largest = numbers[0]
    print(f"Starting with largest = {largest}")
    
    for num in numbers:
        print(f"Checking {num}...")
        if num > largest:
            largest = num
            print(f"  New largest: {largest}")
    
    return largest

print(find_largest([3, 7, 2, 8, 1]))

print("\n2. Improved error handling")
print("-------------------------")

def calculate_average_safe(numbers):
    if not numbers:
        return None
    
    try:
        return sum(numbers) / len(numbers)
    except TypeError as e:
        print(f"Error: All elements must be numbers. {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

print(f"Safe average of [1, 2, 3]: {calculate_average_safe([1, 2, 3])}")
print(f"Safe average of []: {calculate_average_safe([])}")
print(f"Safe average of [1, '2', 3]: {calculate_average_safe([1, '2', 3])}")

print("\n3. Logging - a better alternative to print statements")
print("---------------------------------------------------")

import logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_data(data):
    logging.info(f"Processing data with {len(data)} items")
    
    result = []
    for i, item in enumerate(data):
        try:
            logging.debug(f"Processing item {i}: {item}")
            processed = item * 2  # Simple transformation
            result.append(processed)
            logging.debug(f"Processed result: {processed}")
        except Exception as e:
            logging.error(f"Error processing item {i}: {e}")
    
    logging.info("Data processing complete")
    return result

sample_data = [1, 2, 3, 4, 5]
processed = process_data(sample_data)
print(f"Processed data: {processed}")

print("\n4. Understanding tracebacks")
print("--------------------------")

def level_c():
    # This will cause a NameError
    return undefined_variable

def level_b():
    return level_c()

def level_a():
    return level_b()

try:
    level_a()
except NameError as e:
    print("Error occurred!")
    print("The traceback would show:")
    print("  level_a called level_b")
    print("  level_b called level_c")
    print("  level_c tried to use an undefined_variable")
    print(f"Error message: {e}")

print("\n--- Exercise ---")
print("1. Modify the 'calculate_average' function to handle non-numeric inputs properly.")
print("2. Write a function that validates user input and uses appropriate error handling.")
print("3. Create a function that uses logging instead of print statements.")