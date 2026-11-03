import ast


def bare_excepts(source):
    lines = []
    # ast.ExceptHandler ve node.type is None
    return lines

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
