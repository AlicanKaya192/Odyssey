def missing_fields(record, required):
    return [name for name in required if name not in record]

REQUIRED = ["time", "user", "source", "event", "result"]
print(missing_fields({"time": "10:00", "user": "bob", "event": "login", "result": ""}, REQUIRED))
print(missing_fields(dict.fromkeys(REQUIRED, "x"), REQUIRED))
