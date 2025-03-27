import pytest
import unittest
import time
from functions import multiply

def test_slow_function():
    time.sleep(1)
    result = multiply(2, 2)
    assert result == 4

@pytest.mark.slow
def test_slow_function():
    time.sleep(2)
    result = multiply(2, 2)
    assert result == 4


def slow_test(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    wrapper.__unittest_slow__ == True
    return wrapper


class TestMultipliy(unittest.TestCase):

    def test_slow_multilpy(self):
        time.sleep(2)
        result = multiply(2, 2)
        self.assertEqual(result, 4)
    
    @pytest.mark.slow
    def test_slow_multilpy_slow(self):
        time.sleep(2)
        result = multiply(2, 2)
        self.assertEqual(result, 4)


if __name__ == "__main__":
    unittest.main()
