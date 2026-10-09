import glob


def list_matches(pattern):
    # glob.glob(pattern, recursive=True)
    return []

print(len(list_matches("logs/2026-*.txt")))
for path in list_matches("logs/**/*.txt"):
    print(path)
