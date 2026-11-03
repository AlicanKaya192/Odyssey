def dangerous_calls(source):
    found = []
    for number, line in enumerate(source.splitlines(), 1):
        for name in ("eval", "exec"):
            if name + "(" in line:
                found.append(f"{number}: {name}")
    return found

SOURCE = """# eval( in a comment
x = "exec( in a string"
y = eval(a) + eval(b)
exec(code)
"""
for item in dangerous_calls(SOURCE):
    print(item)
