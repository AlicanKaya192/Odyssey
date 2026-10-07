from http import HTTPStatus

codes = [200, 200, 404, 200, 201, 500, 200, 429, 200, 404,
         200, 304, 200, 404, 503, 200, 201, 200, 429, 404]

counts = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
errors = {}
for code in codes:
    counts[str(code // 100) + "xx"] += 1
    if code >= 400:
        errors[code] = errors.get(code, 0) + 1

for name in ["2xx", "3xx", "4xx", "5xx"]:
    print(name + ":", counts[name])

rate = (counts["4xx"] + counts["5xx"]) / len(codes) * 100
print(f"error rate: {rate:.1f}%")

worst = max(errors, key=errors.get)
print("most common error:", worst, HTTPStatus(worst).phrase)
