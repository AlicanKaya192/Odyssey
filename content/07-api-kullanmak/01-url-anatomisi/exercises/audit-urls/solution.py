from urllib.parse import urlparse

urls = [
    "https://api.example.com/v1/weather?city=Izmir",
    "http://api.example.com/v1/login?user=ada",
    "http://localhost:8000/books",
    "https://api.github.com/repos/python/cpython",
    "http://127.0.0.1:8000/books/42",
    "http://data.example.org/export?format=csv",
]

insecure = []
hosts = {}
for url in urls:
    parts = urlparse(url)
    local = parts.hostname in ("localhost", "127.0.0.1")
    if parts.scheme == "http" and not local:
        insecure.append(url)
    hosts[parts.hostname] = hosts.get(parts.hostname, 0) + 1

print("Insecure:")
for url in insecure:
    print(url)
print("Requests per host:")
for host in sorted(hosts):
    print(host, hosts[host])
