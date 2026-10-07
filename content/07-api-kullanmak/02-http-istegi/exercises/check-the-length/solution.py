good = """POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 37

{"title": "Emma", "author": "Austen"}"""

bad = """POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 50

{"title": "Dune", "author": "Herbert"}"""


def check_length(raw):
    head, body = raw.split("\n\n", 1)
    declared = None
    for line in head.split("\n")[1:]:
        name, value = line.split(": ", 1)
        if name.lower() == "content-length":
            declared = int(value)
    actual = len(body.encode("utf-8"))
    if declared == actual:
        return "ok"
    return "mismatch: declared " + str(declared) + ", actual " + str(actual)


print("good:", check_length(good))
print("bad:", check_length(bad))
