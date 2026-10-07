import json

text = '{"city": "Istanbul", "temp": 18.5, "rain": false, "wind": null}'
data = json.loads(text)

print("city:", data["city"])
print("temp:", data["temp"])
print("rain:", data["rain"])
print("wind:", data["wind"])
print("temp type:", type(data["temp"]).__name__)
