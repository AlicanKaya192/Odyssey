import difflib


def lookalikes(names, popular):
    lines = []
    for name in names:
        close = difflib.get_close_matches(name, popular, n=1, cutoff=0.8)
        if close:
            lines.append(name + " -> " + close[0])
    return lines

POPULAR = ["numpy", "pandas", "django", "flask", "pytest"]
for line in lookalikes(["numpi", "pandas", "flaskk", "leftpad"], POPULAR):
    print(line)
