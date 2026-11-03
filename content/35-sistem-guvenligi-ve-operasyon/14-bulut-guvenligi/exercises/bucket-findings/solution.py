def bucket_findings(buckets):
    lines = []
    for b in sorted(buckets, key=lambda item: item["name"]):
        if b["public"] and b["data"] != "public":
            lines.append(b["name"] + ": public with " + b["data"] + " data")
        if not b["encrypted"]:
            lines.append(b["name"] + ": not encrypted")
    return lines

BUCKETS = [
    {"name": "web", "public": True, "encrypted": True, "data": "public"},
    {"name": "exports", "public": True, "encrypted": False, "data": "personal"},
    {"name": "logs", "public": False, "encrypted": False, "data": "internal"},
]
for line in bucket_findings(BUCKETS):
    print(line)
