raw = """HTTP/1.1 429 Too Many Requests
Content-Type: application/json; charset=utf-8
Retry-After: 30

{"error": "rate limit", "limit": 60}"""

# parse_response(raw): {"code": <int>, "headers": {...}, "body": "..."}


# response = parse_response(raw)
# Yazdir: kod, icerik turu (; oncesi), "wait N seconds", govde
