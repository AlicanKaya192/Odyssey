import tomllib


def check_version(tag, pyproject):
    if not tag.startswith("v"):
        return f"tag {tag} must start with v"
    version = tomllib.loads(pyproject)["project"]["version"]
    if tag != f"v{version}":
        return f"tag {tag} does not match version {version}"
    return "ok"


pyproject = """
[project]
name = "tempconv"
version = "0.3.0"
"""
print(check_version("v0.3.0", pyproject))
print(check_version("v0.3.1", pyproject))
print(check_version("0.3.0", pyproject))
