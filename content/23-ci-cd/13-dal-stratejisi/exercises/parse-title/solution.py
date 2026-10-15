import re

PATTERN = re.compile(r"^(feat|fix|docs|test|chore)(\(([a-z-]+)\))?(!)?: (\S.*)$")


def parse_title(title):
    match = PATTERN.match(title)
    if match is None:
        return None
    kind, _, scope, bang, summary = match.groups()
    return [kind, scope, bang == "!", summary]


titles = [
    "feat(login): remember me",
    "fix!: drop the old api",
    "docs: explain the setup",
    "Fix login bug",
    "chore(deps):bump pytest",
]
for title in titles:
    print(parse_title(title))
