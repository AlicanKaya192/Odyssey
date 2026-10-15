import sys
import tomllib

tag = sys.argv[1]
with open("pyproject.toml", "rb") as handle:
    version = tomllib.load(handle)["project"]["version"]
if tag != "v" + version:
    print(f"tag {tag} does not match version {version}")
    sys.exit(1)
print(f"tag {tag} matches version {version}")
