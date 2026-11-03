def resolve(records, name):
    for _ in range(9):
        record = records.get(name)
        if record is None:
            return "NXDOMAIN"
        kind, value = record
        if kind == "A":
            return value
        name = value
    return "LOOP"

RECORDS = {
    "example.com": ["A", "203.0.113.10"],
    "www.example.com": ["CNAME", "example.com"],
    "a.example": ["CNAME", "b.example"],
    "b.example": ["CNAME", "a.example"],
}
for name in ["www.example.com", "mail.example.com", "a.example"]:
    print(name, resolve(RECORDS, name))
