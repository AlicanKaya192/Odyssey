menu = {
    "/weather": "18 degrees, cloudy",
    "/forecast": "rain tomorrow",
    "/cities": "Istanbul, Ankara, Izmir",
}


def request(path):
    if path in menu:
        return menu[path]
    return "404 Not Found"


print(request("/weather"))
print(request("/cities"))
print(request("/news"))
