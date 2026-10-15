def next_version(current, commits):
    # Find the bump level for each message (3 MAJOR, 2 MINOR, 1 PATCH); the biggest wins.
    pass


print(next_version("1.4.2", ["fix: handle empty cart", "docs: typo"]))
print(next_version("1.4.2", ["fix: a", "feat(api): add search"]))
print(next_version("1.4.2", ["feat!: drop old routes", "fix: b"]))
print(next_version("1.4.2", ["chore: bump deps"]))
