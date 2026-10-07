def next_step(code):
    kind = code // 100
    if kind == 2:
        return "use the body"
    if kind == 3:
        return "follow Location"
    if code in (401, 403):
        return "check your key"
    if code == 404:
        return "check the address"
    if code == 429:
        return "wait, then retry"
    if kind == 4:
        return "fix the request"
    return "retry later"


codes = [200, 201, 301, 401, 403, 404, 422, 429, 500, 503]
for code in codes:
    print(code, "->", next_step(code))
