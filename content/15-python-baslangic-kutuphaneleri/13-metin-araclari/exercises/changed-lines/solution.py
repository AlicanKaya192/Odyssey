import difflib


def changed_lines(old, new):
    diff = difflib.unified_diff(old, new, lineterm="")
    return [line for line in diff
            if line[:1] in "+-" and not line.startswith(("+++", "---"))]

old = ["a = 1", "b = 2", "print(a + b)"]
new = ["a = 1", "b = 3", "print(a + b)", "print('done')"]
for line in changed_lines(old, new):
    print(line)
