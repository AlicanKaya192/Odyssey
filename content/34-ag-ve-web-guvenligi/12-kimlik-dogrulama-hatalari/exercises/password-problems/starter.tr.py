def password_problems(password, user, common):
    problems = []
    if len(password) < 8:
        problems.append("too short")
    return problems

COMMON = ["123456", "password", "qwerty"]
for pw in ["qwerty", "Ada2026!", "blue-river-under-stone", "PASSWORD"]:
    print(pw, password_problems(pw, "ada", COMMON))
