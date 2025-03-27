import pytest

database = {
    "users": [
        {"id": 1, "name": "John", "email": "john@example.com"},
        {"id": 2, "name": "Jane", "email": "jane@example.com"},
    ]
}

def get_user_by_id(user_id):
    return database["users"][user_id - 1]






