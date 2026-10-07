import shlex

import requests


def parse_curl(command):
    parts = shlex.split(command)
    method = None
    url = None
    headers = {}
    data = None
    i = 1
    while i < len(parts):
        part = parts[i]
        if part == "-X":
            method = parts[i + 1]
            i += 2
        elif part == "-H":
            name, value = parts[i + 1].split(": ", 1)
            headers[name] = value
            i += 2
        elif part == "-d":
            data = parts[i + 1]
            i += 2
        else:
            url = part
            i += 1
    if method is None:
        method = "POST" if data is not None else "GET"
    return {"method": method, "url": url, "headers": headers, "data": data}


command = 'curl -X POST http://api.odyssey.test/books -H "Authorization: Bearer letmein" -H "Content-Type: application/json" -d \'{"title": "Kindred", "price": 11.5}\''

# Take it apart with parse_curl, send it with requests.request
# "status: 201", "location: /books/24", "title: Kindred"
