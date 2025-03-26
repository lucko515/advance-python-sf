# 02: Python Debugger (pdb)
print("Python Debugger (pdb)")
print("--------------------")

import pdb

print("\n1. Basic pdb usage with set_trace()")
print("----------------------------------")

def complex_calculation(a, b, c):
    result = a * b
    # This is where you would typically add a breakpoint
    # pdb.set_trace()  # Uncomment to activate debugger
    result = result / c
    return result

# Try with different values
try:
    print(f"Result: {complex_calculation(5, 10, 2)}")  # Should work: 25
    print(f"Result: {complex_calculation(5, 10, 0)}")  # Will cause error
except ZeroDivisionError as e:
    print(f"Error caught: {e}")

print("\nWhen pdb.set_trace() is uncommented and the function runs:")
print("1. The program execution pauses at that line")
print("2. You can inspect variables: p result, p a, p b, p c")
print("3. Step to next line: n")
print("4. Continue execution: c")
print("5. Quit debugger: q")

print("\n2. Debugging a more complex example")
print("---------------------------------")

def process_item(item):
    # Process a single item
    if item < 0:
        return item * -1  # Make positive
    return item * 2

def process_list(items):
    results = []
    for i, item in enumerate(items):
        # pdb.set_trace()  # Uncomment to debug
        processed = process_item(item)
        results.append(processed)
    return results

def analyze_data():
    data = [1, -2, 3, -4, 0]
    # Process the data
    processed_data = process_list(data)
    # Calculate the sum
    total = sum(processed_data)
    # Calculate the average
    average = total / len(processed_data)
    return processed_data, total, average

# Run the analysis
processed, total, avg = analyze_data()
print(f"Processed data: {processed}")
print(f"Total: {total}")
print(f"Average: {avg}")

print("\n3. Post-mortem debugging")
print("-----------------------")

def buggy_function():
    data = {'a': 1, 'b': 2}
    # This will raise a KeyError
    return data['c']

try:
    buggy_function()
except Exception as e:
    print(f"Error caught: {e}")
    print("\nIn a real debugging session, you could now use:")
    print("import pdb; pdb.pm()")
    print("This would start the debugger at the point of the exception")

print("\n4. Breakpoints at specific conditions")
print("----------------------------------")

def process_customer_data(customers):
    results = []
    for i, customer in enumerate(customers):
        # Example of a conditional breakpoint
        # if customer['balance'] < 0:
        #     pdb.set_trace()  # Only debug customers with negative balance
        
        name = customer['name']
        balance = customer['balance']
        
        # Process customer data
        status = "Good" if balance >= 0 else "Overdrawn"
        results.append(f"Customer {name}: {status} (${balance})")
    
    return results

customers = [
    {'name': 'Alice', 'balance': 100},
    {'name': 'Bob', 'balance': -50},
    {'name': 'Charlie', 'balance': 200},
    {'name': 'Dave', 'balance': -10}
]

customer_status = process_customer_data(customers)
for status in customer_status:
    print(status)

print("\n5. Debugging with Python 3.7+ breakpoint() function")
print("------------------------------------------------")

def calculate_statistics(numbers):
    if not numbers:
        return None, None, None
    
    # Sort the numbers
    sorted_nums = sorted(numbers)
    
    # Calculate median
    n = len(sorted_nums)
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    # Here you could use the new breakpoint() function
    # breakpoint()  # This uses pdb.set_trace() internally
    
    # Calculate mean
    mean = sum(sorted_nums) / n
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in sorted_nums) / n
    std_dev = variance ** 0.5
    
    return mean, median, std_dev

data_set = [5, 2, 9, 1, 5, 6]
mean, median, std_dev = calculate_statistics(data_set)
print(f"Data: {data_set}")
print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Standard Deviation: {std_dev:.2f}")
