# To run tests use terminal command: pytest tests.py
import pytest
from functions import add, subtract, divide, multiply

def test_add():
    assert add(1, 2) == 3, "General numbers"
    assert add(-1, 1) == 0, "Negative numbers"
    assert add(0, 0) == 0, "Zeroes"
    assert add(0, 1) == 1, "Zero and number"


def test_divide():
    assert divide(10, 2) == 5
    # assert divide(10, 0) == 0
    assert divide(0, 10) == 0

# -> explain division by zero error

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)




