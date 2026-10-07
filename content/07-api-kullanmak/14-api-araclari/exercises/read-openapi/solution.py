import requests

BASE = "http://api.odyssey.test"

spec = requests.get(BASE + "/openapi.json").json()
print(spec["info"]["title"], spec["info"]["version"])

endpoints = []
secured = 0
for path, operations in spec["paths"].items():
    for method, operation in operations.items():
        line = method.upper() + " " + path + " - " + operation["summary"]
        if "security" in operation:
            line += " (auth)"
            secured += 1
        endpoints.append(line)

for line in endpoints:
    print(line)
print("need auth:", secured)
