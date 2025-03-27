import pytest
import requests

database = {
    "users": [
        {"id": 1, "name": "John", "email": "john@example.com"},
        {"id": 2, "name": "Jane", "email": "jane@example.com"},
    ]
}

def get_user_by_id(user_id):
    return database["users"][user_id - 1]

def fetch_user_data(user_id):
    response = requests.get(f"http://some-webisite.com/userId={user_id}")
    response.raise_for_status()

    response2 = requests.get(f"http://some-webisite.com/userId={user_id}")
    response2.raise_for_status()

    more_info = response2.json()
    clean_response = response.json()
    clean_response['email'] = clean_response['email'].strip().lower()
    
    return {
        "user": clean_response,
        "info": more_info
    }



def method_1():
    return "something"

def method_2():
    return "something"

def method_3():
    return "something"

def method_4():
    return "something"

def main_method():
    raise NotImplementedError


def some_other_method():
    main_method() == 5000