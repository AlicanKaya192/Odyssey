import re

PATTERN = r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+"


def redact(text):
    def mask(match):
        user, domain = match.group(0).split("@", 1)
        return user[0] + "***@" + domain
    return re.sub(PATTERN, mask, text)

print(redact("Owner: ada@example.org"))
print(redact("Seen: b.lee@example.org, x@y.org"))
print(redact("No address here."))
