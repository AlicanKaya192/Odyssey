def dangling(records):
    found = []
    for name, (kind, value) in records.items():
        if kind == "CNAME" and value not in records:
            found.append(name)
    return sorted(found)

RECORDS = {
    "example.com": ["A", "203.0.113.10"],
    "www.example.com": ["CNAME", "example.com"],
    "shop.example.com": ["CNAME", "old-shop.example.net"],
    "blog.example.com": ["CNAME", "pages.example.net"],
    "pages.example.net": ["A", "198.51.100.20"],
}
print(dangling(RECORDS))
