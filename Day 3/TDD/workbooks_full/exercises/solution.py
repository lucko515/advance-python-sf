# -----------------------------------------------------------------------------
# TDD EXERCISE - String Calculator (Solution)
# -----------------------------------------------------------------------------

"""
Solution developed using TDD principles:

1. First wrote test_empty_string
   - Implemented return 0
   - Test passed

2. Added test_single_number
   - Modified code to handle single number
   - Test passed

3. Added test_two_numbers
   - Implemented split and sum
   - Test passed

4. Added test_multiple_numbers
   - Code already handled this case
   - Test passed

Each step followed the TDD cycle:
- Write failing test
- Write minimal code to pass
- Refactor if needed
- Verify all tests pass
"""
import pytest

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
    if not numbers:
        return 0
    return sum(int(num) for num in numbers.split(','))


def test_empty_string():
    """Test that empty string returns 0."""
    assert string_calculator("") == 0

def test_single_number():
    """Test that single number returns that number."""
    assert string_calculator("1") == 1
    assert string_calculator("42") == 42

def test_two_numbers():
    """Test that two numbers are added correctly."""
    assert string_calculator("1,2") == 3
    assert string_calculator("10,20") == 30

def test_multiple_numbers():
    """Test that multiple numbers are added correctly."""
    assert string_calculator("1,2,3") == 6
    assert string_calculator("1,2,3,4,5") == 15