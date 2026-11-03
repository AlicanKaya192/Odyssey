def parse_headers(text):
    headers = {}
    for line in text.split("\n"):
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()
    return headers

text = "Host: shop.example.com\nCookie:  session=abc123 \nbroken line\nX-Mode: test"
for name, value in parse_headers(text).items():
    print(name, "=", value)
