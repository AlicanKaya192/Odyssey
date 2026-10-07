import requests

environment = {"base_url": "http://api.odyssey.test", "token": "letmein"}

collection = [
    {"name": "List books", "method": "GET", "url": "{{base_url}}/books", "headers": {}},
    {"name": "Who am I", "method": "GET", "url": "{{base_url}}/me",
     "headers": {"Authorization": "Bearer {{token}}"}},
    {"name": "Add a book", "method": "POST", "url": "{{base_url}}/books",
     "headers": {"Authorization": "Bearer {{token}}"}, "body": {"title": "Kindred", "price": 11.5}},
    {"name": "Missing book", "method": "GET", "url": "{{base_url}}/books/99", "headers": {}},
]


def fill(text, variables):
    for name, value in variables.items():
        text = text.replace("{{" + name + "}}", value)
    return text


for item in collection:
    url = fill(item["url"], environment)
    headers = {name: fill(value, environment) for name, value in item["headers"].items()}
    r = requests.request(item["method"], url, headers=headers, json=item.get("body"))
    print(item["name"] + ":", r.status_code)
