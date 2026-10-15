import re


def parse_title(title):
    # Write a regular expression; use one group for each part.
    pass


titles = [
    "feat(login): remember me",
    "fix!: drop the old api",
    "docs: explain the setup",
    "Fix login bug",
    "chore(deps):bump pytest",
]
for title in titles:
    print(parse_title(title))
