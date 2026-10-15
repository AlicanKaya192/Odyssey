import sys
import tomllib

tag = sys.argv[1]
with open("pyproject.toml", "rb") as file:
    version = tomllib.load(file)["project"]["version"]
if tag != f"v{version}":
    sys.exit(f"tag {tag} does not match version {version}")
print(f"tag {tag} matches version {version}")
