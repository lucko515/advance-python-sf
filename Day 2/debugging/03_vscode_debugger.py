# 03: VS Code Debugger for Python
print("VS Code Debugger for Python")
print("-------------------------")

# Note: This file contains code examples that you'll use to demonstrate
# VS Code's debugging capabilities. You'll need to show the debugging
# UI and functionality interactively.

print("\n1. Basic Debugging with VS Code")
print("-----------------------------")

def calculate_factorial(n):
    """Calculate the factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        # Good place for a breakpoint
        result *= i
    
    return result

try:
    # Try with different values to demonstrate debugging
    n = 5
    print(f"Factorial of {n} is {calculate_factorial(n)}")
except ValueError as e:
    print(f"Error: {e}")

print("\nTo debug this function in VS Code:")

print("\n2. Debugging with Watch Expressions")
print("---------------------------------")

def analyze_string(text):
    """Analyze a string and return statistics."""
    if not text:
        return {
            'length': 0,
            'words': 0,
            'lines': 0,
            'characters': {}
        }
    
    # Count words and lines
    words = text.split()
    lines = text.split('\n')
    
    # Count character frequencies
    char_count = {}
    for char in text:
        # Good place for a breakpoint to watch char_count
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    return {
        'length': len(text),
        'words': len(words),
        'lines': len(lines),
        'characters': char_count
    }

sample_text = """This is a sample text.
It has multiple lines.
We will analyze it with VS Code's debugger."""

result = analyze_string(sample_text)
print(f"Text analysis result:")
print(f"- Length: {result['length']} characters")
print(f"- Words: {result['words']}")
print(f"- Lines: {result['lines']}")
print(f"- Most common character: {max(result['characters'].items(), key=lambda x: x[1])}")

print("\n3. Conditional Breakpoints")
print("-------------------------")

def process_transactions(transactions):
    """Process a list of financial transactions."""
    total = 0
    for i, transaction in enumerate(transactions):
        # Set a conditional breakpoint here: transaction['amount'] < 0
        description = transaction['description']
        amount = transaction['amount']
        
        # Process the transaction
        total += amount
        
        # Print a summary
        transaction_type = "DEPOSIT" if amount > 0 else "WITHDRAWAL"
        print(f"Transaction {i+1}: {transaction_type} - {description} (${abs(amount):.2f})")
    
    return total

transactions = [
    {'description': 'Salary', 'amount': 2000.00},
    {'description': 'Rent', 'amount': -1000.00},
    {'description': 'Groceries', 'amount': -150.50},
    {'description': 'Refund', 'amount': 75.00},
    {'description': 'Dining out', 'amount': -45.75}
]

balance = process_transactions(transactions)
print(f"Final balance: ${balance:.2f}")

print("\n4. Logpoints - Debugging without Pausing")
print("--------------------------------------")

def validate_user_data(user):
    """Validate user data for a registration form."""
    errors = []
    
    # Check name (set a logpoint here with message: "Checking name: {user['name']}")
    if not user['name'] or len(user['name']) < 2:
        errors.append("Name must be at least 2 characters")
    
    # Check email (set a logpoint here)
    if not user['email'] or '@' not in user['email']:
        errors.append("Invalid email address")
    
    # Check age (set a logpoint here)
    if not isinstance(user['age'], int) or user['age'] < 18:
        errors.append("Must be at least 18 years old")
    
    # Check password (set a logpoint here)
    if not user['password'] or len(user['password']) < 8:
        errors.append("Password must be at least 8 characters")
    
    return errors

test_users = [
    {'name': 'John Doe', 'email': 'john@example.com', 'age': 25, 'password': 'securepass123'},
    {'name': 'J', 'email': 'not-an-email', 'age': 17, 'password': 'short'}
]

for i, user in enumerate(test_users):
    print(f"\nValidating user {i+1}: {user['name']}")
    validation_errors = validate_user_data(user)
    
    if validation_errors:
        print(f"Found {len(validation_errors)} errors:")
        for error in validation_errors:
            print(f"- {error}")
    else:
        print("User data is valid")

print("\n5. Debugging with Multiple Files")
print("-----------------------------")

# We'll use these functions to demonstrate stepping between files
# In a real demo, these would be in separate files

def main_function():
    """Main function that calls other functions."""
    print("Starting main function")
    
    data = [5, 10, 15, 20, 25]
    result = helper_function(data)
    
    processed = final_calculation(result)
    print(f"Final result: {processed}")
    return processed

def helper_function(data):
    """Helper function that processes data."""
    print("Processing in helper function")
    
    result = 0
    for item in data:
        # Good place for a breakpoint
        result += item * 2
    
    return result

def final_calculation(value):
    """Final calculation based on the helper result."""
    print("Performing final calculation")
    
    # Another good place for a breakpoint
    return value / 2

# Call the main function to demonstrate stepping between functions
main_function()