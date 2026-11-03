ALLOWED = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def parse_request_line(line):
    parts = line.split(" ")
    # uc parca mi, yontem izinli mi, yol / ile mi basliyor?
    return parts

for line in ["GET /cart HTTP/1.1", "BREW /pot HTTP/1.1",
             "GET cart HTTP/1.1", "POST /login"]:
    print(parse_request_line(line))
