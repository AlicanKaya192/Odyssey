responses = [
    {"url": "/home", "content_type": "text/html"},
    {"url": "/api/weather", "content_type": "application/json"},
    {"url": "/about", "content_type": "text/html"},
    {"url": "/api/cities", "content_type": "application/json"},
    {"url": "/api/forecast", "content_type": "application/json"},
]

api_urls = []
people = 0
for response in responses:
    if response["content_type"] == "application/json":
        api_urls.append(response["url"])
    elif response["content_type"] == "text/html":
        people += 1

print("For programs:")
for url in api_urls:
    print(url)
print("For people:", people)
