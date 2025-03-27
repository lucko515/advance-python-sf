import pytest
from source.functions import divide

def test_divide():
    assert divide(10, 2) == 5
    assert divide(0, 10) == 0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)