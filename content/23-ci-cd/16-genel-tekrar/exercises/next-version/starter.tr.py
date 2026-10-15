def next_version(current, commits):
    # Her mesaj icin artis duzeyini bul (3 ANA, 2 YAN, 1 YAMA); en buyugu kazanir.
    pass


print(next_version("1.4.2", ["fix: handle empty cart", "docs: typo"]))
print(next_version("1.4.2", ["fix: a", "feat(api): add search"]))
print(next_version("1.4.2", ["feat!: drop old routes", "fix: b"]))
print(next_version("1.4.2", ["chore: bump deps"]))
