def dangling(records):
    found = []
    # find CNAMEs whose target is not in the records
    return found

RECORDS = {
    "example.com": ["A", "203.0.113.10"],
    "www.example.com": ["CNAME", "example.com"],
    "shop.example.com": ["CNAME", "old-shop.example.net"],
    "blog.example.com": ["CNAME", "pages.example.net"],
    "pages.example.net": ["A", "198.51.100.20"],
}
print(dangling(RECORDS))
