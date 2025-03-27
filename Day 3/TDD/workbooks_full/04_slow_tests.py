import pytest
import time
from functions import multiply

def test_slow_function():
    time.sleep(1)
    result = multiply(2, 3)
    assert result == 6


@pytest.mark.slow
def test_slow_function_slow():
    time.sleep(6)
    result = multiply(2, 3)
    assert result == 6



