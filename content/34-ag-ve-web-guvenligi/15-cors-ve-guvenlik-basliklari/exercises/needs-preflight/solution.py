SIMPLE_METHODS = {"GET", "HEAD", "POST"}
SIMPLE_HEADERS = {"accept", "accept-language", "content-language", "content-type"}
SIMPLE_TYPES = {
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
}


def needs_preflight(method, headers):
    if method not in SIMPLE_METHODS:
        return True
    for name, value in headers.items():
        name = name.lower()
        if name not in SIMPLE_HEADERS:
            return True
        if name == "content-type" and value.split(";")[0].strip().lower() not in SIMPLE_TYPES:
            return True
    return False

print(needs_preflight("GET", {}))
print(needs_preflight("POST", {"Content-Type": "text/plain"}))
print(needs_preflight("POST", {"Content-Type": "application/json"}))
print(needs_preflight("GET", {"X-Api-Key": "k"}))
print(needs_preflight("PUT", {}))
