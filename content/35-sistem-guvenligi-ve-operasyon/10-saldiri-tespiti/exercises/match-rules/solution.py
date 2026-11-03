import re


def match_rules(lines, rules):
    found = []
    for number, line in enumerate(lines, 1):
        for name in sorted(rules):
            if re.search(rules[name], line):
                found.append(f"{number}: {name}")
    return found

RULES = {
    "path traversal": r"\.\./",
    "script tag": r"(?i)<script",
}
LINES = [
    "GET /index.html",
    "GET /files?name=../x",
    "POST /c body=<SCRIPT>../",
]
for item in match_rules(LINES, RULES):
    print(item)
