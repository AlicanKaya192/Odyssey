import ast

WORDS = ("password", "secret", "token")


def hardcoded_secrets(source):
    names = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign):
            # deger sabit bir metin mi? adi supheli mi?
            pass
    return sorted(names)

CODE = """
db_password = "hunter2"
api_token = load_from_vault("api")
retries = 3
SECRET_KEY = "dev-key-123"
admin_secret = 42
"""
print(hardcoded_secrets(CODE))
