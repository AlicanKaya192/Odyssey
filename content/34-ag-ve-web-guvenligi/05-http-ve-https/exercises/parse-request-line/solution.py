ALLOWED = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def parse_request_line(line):
    parts = line.split(" ")
    if len(parts) != 3:
        return None
    method, path, version = parts
    if method not in ALLOWED or not path.startswith("/"):
        return None
    return [method, path, version]

for line in ["GET /cart HTTP/1.1", "BREW /pot HTTP/1.1",
             "GET cart HTTP/1.1", "POST /login"]:
    print(parse_request_line(line))
