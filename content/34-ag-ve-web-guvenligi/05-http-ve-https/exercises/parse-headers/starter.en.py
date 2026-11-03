def parse_headers(text):
    headers = {}
    # split each line at the first :
    return headers

text = "Host: shop.example.com\nCookie:  session=abc123 \nbroken line\nX-Mode: test"
for name, value in parse_headers(text).items():
    print(name, "=", value)
