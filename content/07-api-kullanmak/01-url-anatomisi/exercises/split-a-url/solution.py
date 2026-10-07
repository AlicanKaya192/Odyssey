from urllib.parse import urlparse

url = "https://api.weather.test:9000/v2/forecast?city=Izmir&days=3#top"
parts = urlparse(url)

print("scheme:", parts.scheme)
print("host:", parts.hostname)
print("port:", parts.port)
print("path:", parts.path)
print("query:", parts.query)
print("fragment:", parts.fragment)
