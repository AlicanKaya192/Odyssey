raw = """GET /v1/books HTTP/1.1
Host: localhost:8000
ACCEPT: application/json
user-agent: odyssey-client/1.0"""

lines = raw.split("\n")
headers = {}
for line in lines[1:]:
    name, value = line.split(": ", 1)
    headers[name.lower()] = value

print("host:", headers["host"])
print("accept:", headers["accept"])
print("has authorization:", "authorization" in headers)
