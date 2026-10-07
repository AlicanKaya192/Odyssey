def parse_status_line(line):
    version, code, reason = line.split(" ", 2)
    return {"version": version, "code": int(code), "reason": reason}


lines = [
    "HTTP/1.1 200 OK",
    "HTTP/1.1 404 Not Found",
    "HTTP/1.1 429 Too Many Requests",
    "HTTP/1.1 201 Created",
]
successful = 0
for line in lines:
    status = parse_status_line(line)
    print(status["code"], "|", status["reason"])
    if 200 <= status["code"] < 300:
        successful += 1
print("successful:", successful)
