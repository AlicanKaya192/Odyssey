# parse_status_line(line): {"version": ..., "code": <int>, "reason": ...}


lines = [
    "HTTP/1.1 200 OK",
    "HTTP/1.1 404 Not Found",
    "HTTP/1.1 429 Too Many Requests",
    "HTTP/1.1 201 Created",
]
# For each line "404 | Not Found"; at the end "successful: N"
