def bump(version, part):
    major, minor, patch = (int(p) for p in version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def next_version(version, messages):
    # Her mesaj icin bir seviye bul (0 yok, 1 yama, 2 yan, 3 ana); en buyugunu tut.
    pass


print(next_version("1.4.2", ["fix: handle empty input", "docs: fix typo"]))
print(next_version("1.4.2", ["feat: add export", "fix: crash on start"]))
print(next_version("1.4.2", ["fix(cli): wrong flag", "feat!: new config format"]))
print(next_version("1.4.2", ["ci: cache pip", "test: more cases"]))
print(next_version("0.9.0", ["refactor: split module", "chore: BREAKING CHANGE in api"]))
