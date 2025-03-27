"""
Exercise: String Calculator using Test-Driven Development (TDD)

Your task is to implement a string calculator and its tests following TDD principles.
Write tests first, then implement the function to make them pass.

Requirements:
1. Function takes a string of comma-separated numbers
2. Returns their sum as an integer
3. Special cases:
   - Empty string returns 0
   - Single number returns that number
   - Multiple numbers are summed

Examples:
- "" → 0
- "1" → 1
- "1,2" → 3
- "1,2,3" → 6

Tasks:
1. Write test_empty_string first
2. Implement minimal code to pass
3. Write test_single_number
4. Modify code to pass
5. Continue with remaining tests
6. Refactor if needed

Tips:
- Use pytest for testing
- Follow Red-Green-Refactor cycle
- Write only enough code to pass current test
"""

def string_calculator(numbers: str) -> int:
    """
    Calculate sum of comma-separated numbers in a string.
    
    Args:
        numbers: String of comma-separated numbers (e.g., "1,2,3")
        
    Returns:
        Sum of numbers, or 0 for empty string
        
    Examples:
        >>> string_calculator("")
        0
        >>> string_calculator("1")
        1
        >>> string_calculator("1,2")
        3
    """
    # TODO: Implement this function
    if len(numbers) == 0:
        return 0
    
    return sum(map(int, numbers.replace(".", "").split(",")))
