import re


def unpinned(lines):
    names = []
    for line in lines:
        line = line.split("#")[0].strip()
        if not line or "==" in line:
            continue
        names.append(re.split(r"[<>=!~ ;\[]", line)[0])
    return names

LINES = [
    "numpy==2.1.3",
    "pandas>=2.0",
    "",
    "# tools",
    "flask",
    "pytest==8.3.4  # tests",
    "httpkit~=1.0",
]
print(unpinned(LINES))
