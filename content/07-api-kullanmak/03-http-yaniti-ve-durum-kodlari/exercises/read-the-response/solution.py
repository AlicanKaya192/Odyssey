raw = """HTTP/1.1 429 Too Many Requests
Content-Type: application/json; charset=utf-8
Retry-After: 30

{"error": "rate limit", "limit": 60}"""


def parse_response(raw):
    head, body = raw.split("\n\n", 1)
    lines = head.split("\n")
    code = int(lines[0].split(" ", 2)[1])
    headers = {}
    for line in lines[1:]:
        name, value = line.split(": ", 1)
        headers[name.lower()] = value
    return {"code": code, "headers": headers, "body": body}


response = parse_response(raw)
print(response["code"])
print(response["headers"]["content-type"].split(";")[0])
print("wait", int(response["headers"]["retry-after"]), "seconds")
print(response["body"])
