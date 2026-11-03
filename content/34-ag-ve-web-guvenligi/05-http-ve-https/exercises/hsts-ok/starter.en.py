ONE_YEAR = 31536000


def hsts_ok(value):
    # split on ;, find the max-age directive
    return False

for value in ["max-age=31536000; includeSubDomains", "max-age=300",
              "MAX-AGE=63072000", "includeSubDomains", "max-age=abc"]:
    print(hsts_ok(value))
