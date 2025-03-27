import pytest
from functions import divide

class TestClass:

    def __init__(self):
        self.state = 5

    def change_state(self, value):
        self.state = value

    def get_state(self):
        return self.state

@pytest.fixture()
def shared_state():
    return TestClass()

def test_1(shared_state):
    ins = shared_state
    ins.change_state(100)
    assert ins.get_state() == 100

def test_2(shared_state):
    ins = shared_state
    assert ins.get_state() == 5