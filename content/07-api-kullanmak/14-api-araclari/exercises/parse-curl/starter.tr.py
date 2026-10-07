import shlex

# parse_curl(command): {"method", "url", "headers", "data"}


commands = [
    "curl http://api.odyssey.test/books/1",
    "curl -H \"X-API-Key: demo-key-123\" http://api.odyssey.test/stats",
    'curl -X POST http://api.odyssey.test/books -H "Authorization: Bearer letmein" -H "Content-Type: application/json" -d \'{"title": "Kindred", "price": 11.5}\'',
]
# Her komut: "POST http://api.odyssey.test/books 2 {...}"
