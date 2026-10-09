import json
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int


def oldest_user(text):
    # json.loads, User(**d), max(..., key=...)
    return ""

text = '[{"name": "ada", "age": 36}, {"name": "grace", "age": 85}]'
print(oldest_user(text))
