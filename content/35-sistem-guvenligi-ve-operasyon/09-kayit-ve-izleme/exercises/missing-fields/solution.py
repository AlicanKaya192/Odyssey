def missing_fields(record, required):
    return sorted(name for name in required if not record.get(name))

REQUIRED = ["time", "user", "source", "event", "result"]
print(missing_fields({"time": "10:00", "user": "bob", "event": "login", "result": ""}, REQUIRED))
print(missing_fields(dict.fromkeys(REQUIRED, "x"), REQUIRED))
