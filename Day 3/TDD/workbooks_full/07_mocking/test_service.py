import pytest
from service import get_user_by_id

import unittest.mock as mock


@mock.patch("service.get_user_by_id")
def test_get_user_by_id(THIS_IS_A_MOCK):
    THIS_IS_A_MOCK.return_value = {"id": 1, "name": "John", "email": "john@example.com"}

    user_name = get_user_by_id(1)
    
    assert user_name == {"id": 1, "name": "John", "email": "john@example.com"}
