import json

with open("forecast.json", encoding="utf-8") as handle:
    data = json.load(handle)

hottest = None
best = None
for day in data["forecast"]:
    wind = day.get("wind", {})
    print(day["day"], day["temp"], "wind", wind.get("speed", "?"))
    if best is None or day["temp"] > best:
        best = day["temp"]
        hottest = day["day"]

print("hottest:", hottest)
