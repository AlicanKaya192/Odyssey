ALLOWED = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def parse_request_line(line):
    parts = line.split(" ")
    # three parts, allowed method, path starting with /?
    return parts

for line in ["GET /cart HTTP/1.1", "BREW /pot HTTP/1.1",
             "GET cart HTTP/1.1", "POST /login"]:
    print(parse_request_line(line))
