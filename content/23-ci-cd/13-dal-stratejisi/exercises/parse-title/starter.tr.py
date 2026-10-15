import re


def parse_title(title):
    # Bir duzenli ifade yaz; her parca icin bir grup kullan.
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
