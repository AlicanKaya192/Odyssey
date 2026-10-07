good = """POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 37

{"title": "Emma", "author": "Austen"}"""

bad = """POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 50

{"title": "Dune", "author": "Herbert"}"""

# check_length(raw): "ok" ya da "mismatch: declared X, actual Y"


# Iki istegi denetle ve sonucu yazdir:
# print("good:", check_length(good))
# print("bad:", check_length(bad))
