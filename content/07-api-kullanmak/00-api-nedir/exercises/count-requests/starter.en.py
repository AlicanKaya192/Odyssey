# Server log: (client, endpoint)
log = [
    ("app", "/weather"),
    ("web", "/weather"),
    ("app", "/cities"),
    ("bot", "/news"),
    ("app", "/weather"),
    ("web", "/forecast"),
    ("bot", "/news"),
    ("app", "/forecast"),
]
known = ["/weather", "/forecast", "/cities"]

# 1) counts: number of requests per endpoint


# 2) Print "endpoint count" in alphabetical order


# 3) Requests that went to unknown endpoints: "404 responses: N"
