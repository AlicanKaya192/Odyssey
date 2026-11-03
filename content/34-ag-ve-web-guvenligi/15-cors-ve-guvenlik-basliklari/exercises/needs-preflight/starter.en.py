SIMPLE_METHODS = {"GET", "HEAD", "POST"}
SIMPLE_HEADERS = {"accept", "accept-language", "content-language", "content-type"}
SIMPLE_TYPES = {
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
}


def needs_preflight(method, headers):
    return method not in SIMPLE_METHODS

print(needs_preflight("GET", {}))
print(needs_preflight("POST", {"Content-Type": "text/plain"}))
print(needs_preflight("POST", {"Content-Type": "application/json"}))
print(needs_preflight("GET", {"X-Api-Key": "k"}))
print(needs_preflight("PUT", {}))
