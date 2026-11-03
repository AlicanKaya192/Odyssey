import ast


def bare_excepts(source):
    lines = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            lines.append(node.lineno)
    return sorted(lines)

CODE = """
try:
    check_permission(user)
except:
    pass
try:
    load(path)
except FileNotFoundError:
    pass
try:
    verify(token)
except:
    allow = True
"""
print(bare_excepts(CODE))
