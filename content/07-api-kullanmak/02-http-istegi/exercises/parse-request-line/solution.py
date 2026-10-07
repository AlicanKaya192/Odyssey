def parse_request_line(line):
    method, target, version = line.split(" ")
    return {"method": method, "target": target, "version": version}


lines = [
    "GET /v1/books?author=Austen HTTP/1.1",
    "POST /v1/books HTTP/1.1",
    "DELETE /v1/books/42 HTTP/2",
]
for line in lines:
    parts = parse_request_line(line)
    print(parts["method"], "->", parts["target"])
