import re

PATTERN = re.compile(r"\b(gets|strcpy|strcat|sprintf)\s*\(")


def risky_calls(lines):
    found = []
    for number, line in enumerate(lines, 1):
        for match in PATTERN.finditer(line):
            found.append(f"{number}: {match.group(1)}")
    return found

SOURCE = [
    "char name[8];",
    "fgets(name, sizeof name, stdin);",
    "strcpy(copy, name);",
    'snprintf(out, 16, "%s", name);',
    "gets(line); strcat(line, tail);",
]
for item in risky_calls(SOURCE):
    print(item)
