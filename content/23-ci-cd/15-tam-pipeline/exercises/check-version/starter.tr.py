import tomllib


def check_version(tag, pyproject):
    # Once etiketin basini denetle, sonra surumu oku ve karsilastir.
    pass


pyproject = """
[project]
name = "tempconv"
version = "0.3.0"
"""
print(check_version("v0.3.0", pyproject))
print(check_version("v0.3.1", pyproject))
print(check_version("0.3.0", pyproject))
