temps = {"Istanbul": 18, "Ankara": 12, "Izmir": 22}


def server(city):
    if city in temps:
        return {"status": 200, "temp": temps[city]}
    return {"status": 404, "error": "unknown city"}


cities = ["Istanbul", "Paris", "Izmir"]
for city in cities:
    response = server(city)
    if response["status"] == 200:
        print(city + ":", response["temp"])
    else:
        print(city + ": error", response["status"], "(" + response["error"] + ")")
