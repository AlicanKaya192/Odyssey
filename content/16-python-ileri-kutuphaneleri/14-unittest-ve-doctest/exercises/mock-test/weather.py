def fetch_temp(city):
    raise ConnectionError("no network")


def advice(city):
    temp = fetch_temp(city)
    if temp < 10:
        return "coat"
    return "t-shirt"
