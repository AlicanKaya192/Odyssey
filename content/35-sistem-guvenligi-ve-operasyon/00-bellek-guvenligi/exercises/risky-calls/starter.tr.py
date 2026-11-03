def risky_calls(lines):
    found = []
    for number, line in enumerate(lines, 1):
        for name in ["gets", "strcpy", "strcat", "sprintf"]:
            if name in line:
                found.append(f"{number}: {name}")
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
