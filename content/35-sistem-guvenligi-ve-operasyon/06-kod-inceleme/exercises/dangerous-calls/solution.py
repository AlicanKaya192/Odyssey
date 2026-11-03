import ast

DANGEROUS = {"eval", "exec"}


def dangerous_calls(source):
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") in DANGEROUS:
            found.append((node.lineno, node.col_offset, node.func.id))
    return [f"{line}: {name}" for line, col, name in sorted(found)]

SOURCE = """# eval( in a comment
x = "exec( in a string"
y = eval(a) + eval(b)
exec(code)
"""
for item in dangerous_calls(SOURCE):
    print(item)
