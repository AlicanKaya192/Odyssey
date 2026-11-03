def bucket_findings(buckets):
    lines = []
    for b in buckets:
        if b["public"]:
            lines.append(b["name"] + ": public with " + b["data"] + " data")
    return lines

BUCKETS = [
    {"name": "web", "public": True, "encrypted": True, "data": "public"},
    {"name": "exports", "public": True, "encrypted": False, "data": "personal"},
    {"name": "logs", "public": False, "encrypted": False, "data": "internal"},
]
for line in bucket_findings(BUCKETS):
    print(line)
