import re


def mask(line):
    return re.sub(r"(password)=[^&\s]+", r"\1=***", line)

print(mask("user=ada&password=s3cret"))
print(mask("token=abc123 api_key=K9x status=200"))
print(mask("nothing secret here"))
