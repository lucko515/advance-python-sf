import pytest
from source.function import string_calculator

# TODO: Write your tests below
def test_empty_string():
    """Test that empty string returns 0."""
    assert string_calculator("") == 0

def test_single_number():
    """Test that single number returns that number."""
    assert string_calculator("1") == 1

def test_two_numbers():
    """Test that two numbers are added correctly."""
    assert string_calculator("1,2") == 3

def test_multiple_numbers():
    """Test that multiple numbers are added correctly."""
    assert string_calculator("3,3,3") == 9

def test_negative_numbers():
    """Test that negative numbers are added correctly."""
    assert string_calculator("-1,-2,-3") == -6

def test_mixed_numbers():
    """Test that mixed numbers are added correctly."""
    assert string_calculator("1,-2,3") == 2

def test_wrong_input():
    assert string_calculator("1.2.3,4,5") == 132