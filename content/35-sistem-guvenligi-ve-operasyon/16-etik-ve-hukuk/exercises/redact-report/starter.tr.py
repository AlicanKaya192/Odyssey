import re

PATTERN = r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+"


def redact(text):
    return re.sub(PATTERN, "***", text)

print(redact("Owner: ada@example.org"))
print(redact("Seen: b.lee@example.org, x@y.org"))
print(redact("No address here."))
