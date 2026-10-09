import glob


def list_matches(pattern):
    found = glob.glob(pattern, recursive=True)
    return sorted(path.replace("\\", "/") for path in found)

print(len(list_matches("logs/2026-*.txt")))
for path in list_matches("logs/**/*.txt"):
    print(path)
