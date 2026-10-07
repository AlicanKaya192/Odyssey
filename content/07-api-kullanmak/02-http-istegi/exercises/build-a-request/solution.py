def build_request(method, target, host, body=""):
    lines = [method + " " + target + " HTTP/1.1", "Host: " + host]
    if body:
        lines.append("Content-Type: application/json")
        lines.append("Content-Length: " + str(len(body.encode("utf-8"))))
    return "\n".join(lines) + "\n\n" + body


print(build_request("GET", "/v1/books?author=Austen", "api.example.com"))
print("---")
print(build_request("POST", "/v1/books", "api.example.com", '{"title": "Emma"}'))
