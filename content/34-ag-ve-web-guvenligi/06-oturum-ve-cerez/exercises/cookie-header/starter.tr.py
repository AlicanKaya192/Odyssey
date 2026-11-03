def cookie_header(name, value, max_age):
    return f"{name}={value}; Path=/"

for part in cookie_header("session", "abc123", 3600).split("; "):
    print(part)
