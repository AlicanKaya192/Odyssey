def endpoint_url(base, path):
    return base.rstrip("/") + "/" + path.lstrip("/")


print(endpoint_url("https://api.example.com/v1", "weather"))
print(endpoint_url("https://api.example.com/v1/", "/weather"))
print(endpoint_url("https://api.example.com/v1/", "weather"))
print(endpoint_url("https://api.example.com/v1", "/books/42"))
