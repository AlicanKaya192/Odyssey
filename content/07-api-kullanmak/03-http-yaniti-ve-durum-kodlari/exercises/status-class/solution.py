def status_class(code):
    kind = code // 100
    if kind == 1:
        return "info"
    if kind == 2:
        return "success"
    if kind == 3:
        return "redirect"
    if kind == 4:
        return "client error"
    return "server error"


codes = [200, 201, 304, 404, 429, 500, 503]
for code in codes:
    print(code, status_class(code))
