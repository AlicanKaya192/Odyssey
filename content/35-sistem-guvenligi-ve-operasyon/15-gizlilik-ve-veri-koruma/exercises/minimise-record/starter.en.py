def minimise(record, allowed):
    result = {}
    for name in allowed:
        result[name] = record.get(name)
    return result

RECORD = {
    "name": "Ada",
    "email": "ada@example.org",
    "phone": "555-0100",
    "birth_date": "1990-05-01",
}
result = minimise(RECORD, ["email", "phone", "fax"])
for key in sorted(result):
    print(key, result[key])
