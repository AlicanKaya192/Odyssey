import re
import sys

PATTERN = r"^(feat|fix|docs|test|chore)(\([a-z-]+\))?!?: \S.*$"

title = sys.argv[1]
if re.match(PATTERN, title):
    print("title ok")
else:
    print(f"bad title: {title!r}")
    print("expected something like: fix(login): handle empty password")
    sys.exit(1)
