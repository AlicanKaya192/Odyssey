# The temperatures the server knows.
temps = {"Istanbul": 18, "Ankara": 12, "Izmir": 22}

# server(city): if known return {"status": 200, "temp": ...},
# otherwise return {"status": 404, "error": "unknown city"}.


# Client: ask the server about every city and print the result.
cities = ["Istanbul", "Paris", "Izmir"]
