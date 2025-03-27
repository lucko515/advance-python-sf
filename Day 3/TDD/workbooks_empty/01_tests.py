# To run tests use terminal command: pytest tests.py
import pytest
from functions import add, subtract, divide, multiply

def test_add():
    assert add(2, 2) == 4
    assert add(1, -1) == 0
    assert add(10, 0) == 10

def test_add_zeros():
    assert add(0, 0) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(5, 2) == 2.5

def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        divide(100, 0)






