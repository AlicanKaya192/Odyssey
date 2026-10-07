from urllib.parse import parse_qs

query = "city=Ankara&units=imperial&tag=sea&tag=museum&tag=castle"
params = parse_qs(query)

city = params["city"][0]
units = params["units"][0]
tags = params["tag"]

print(city)
print(units)
print(len(tags), "tags:", ", ".join(tags))
