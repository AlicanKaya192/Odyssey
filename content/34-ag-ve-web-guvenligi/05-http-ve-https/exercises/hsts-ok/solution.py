ONE_YEAR = 31536000


def hsts_ok(value):
    for part in value.split(";"):
        name, _, arg = part.strip().partition("=")
        if name.strip().lower() == "max-age":
            arg = arg.strip()
            return arg.isdigit() and int(arg) >= ONE_YEAR
    return False

for value in ["max-age=31536000; includeSubDomains", "max-age=300",
              "MAX-AGE=63072000", "includeSubDomains", "max-age=abc"]:
    print(hsts_ok(value))
