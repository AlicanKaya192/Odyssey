import ast

WORDS = ("password", "secret", "token")


def hardcoded_secrets(source):
    names = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assign):
            continue
        if not (isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
            continue
        for target in node.targets:
            name = getattr(target, "id", "")
            if any(word in name.lower() for word in WORDS):
                names.append(name)
    return sorted(names)

CODE = """
db_password = "hunter2"
api_token = load_from_vault("api")
retries = 3
SECRET_KEY = "dev-key-123"
admin_secret = 42
"""
print(hardcoded_secrets(CODE))
