import json
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int


def oldest_user(text):
    users = [User(**d) for d in json.loads(text)]
    return max(users, key=lambda u: u.age).name

text = '[{"name": "ada", "age": 36}, {"name": "grace", "age": 85}]'
print(oldest_user(text))
