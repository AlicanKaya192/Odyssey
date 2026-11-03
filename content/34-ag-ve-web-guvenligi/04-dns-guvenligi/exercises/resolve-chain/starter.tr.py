def resolve(records, name):
    record = records.get(name)
    if record is None:
        return "NXDOMAIN"
    return record[1]

RECORDS = {
    "example.com": ["A", "203.0.113.10"],
    "www.example.com": ["CNAME", "example.com"],
    "a.example": ["CNAME", "b.example"],
    "b.example": ["CNAME", "a.example"],
}
for name in ["www.example.com", "mail.example.com", "a.example"]:
    print(name, resolve(RECORDS, name))
