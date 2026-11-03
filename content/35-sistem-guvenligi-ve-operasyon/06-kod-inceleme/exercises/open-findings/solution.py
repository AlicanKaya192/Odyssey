def has_reason(line):
    mark = "# nosec: "
    if mark not in line:
        return False
    return line.split(mark, 1)[1].strip() != ""


def open_findings(findings, lines):
    result = []
    for number, message in sorted(findings):
        if not has_reason(lines[number - 1]):
            result.append(f"{number}: {message}")
    return result

LINES = [
    "x = eval(a)  # nosec: a is a constant",
    "y = eval(b)  # nosec",
    "z = eval(c)",
]
FINDINGS = [[3, "eval"], [1, "eval"], [2, "eval"]]
for item in open_findings(FINDINGS, LINES):
    print(item)
