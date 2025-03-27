import pytest
from functions import divide

class TestClass:

    def __init__(self):
        self.state = 5

    def change_state(self, value):
        self.state = value

    def get_state(self):
        return self.state

