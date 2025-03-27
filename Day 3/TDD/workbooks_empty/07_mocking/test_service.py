import pytest
from service import get_user_by_id, fetch_user_data

import unittest.mock as mock
from unittest.mock import patch, MagicMock


@mock.patch("service.get_user_by_id")
def test_get_user_by_id(THIS_IS_A_MOCK):
    THIS_IS_A_MOCK.return_value = {"id": 1, "name": "John", "email": "john@example.com"}

    user_name = get_user_by_id(1)
    
    assert user_name == {"id": 1, "name": "John", "email": "john@example.com"}

@patch("service.requests.get")
def test_fetch_user_data(mock_get):

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "John",
        "email": "    JOHN@example.com    ",
    }

    mock_response2 = MagicMock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = {
        "description": "Hello World",
        "image": "SOME_URL"
    }

    mock_get.side_effect = [mock_response, mock_response2]

    result = fetch_user_data(1)

    assert result['user']['name'] == "John"
    assert result['user']['email'] == 'john@example.com'
    assert result['info']['description'] == 'Hello World'
