import re

PATTERN = re.compile(r"(password|token|secret|api_key)=\S+", re.IGNORECASE)


def redact(line):
    return PATTERN.sub(r"\1=***", line)

print(redact("login user=ada password=hunter2 ok"))
print(redact("api_key=K1 Token=T2 status=200"))
print(redact("nothing to hide here"))
