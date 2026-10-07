# parse_request_line(line): {"method": ..., "target": ..., "version": ...}


lines = [
    "GET /v1/books?author=Austen HTTP/1.1",
    "POST /v1/books HTTP/1.1",
    "DELETE /v1/books/42 HTTP/2",
]
# For each line: "GET -> /v1/books?author=Austen"
