def password_problems(password, user, common):
    problems = []
    if len(password) < 8:
        problems.append("too short")
    if password.lower() in common:
        problems.append("common")
    if user.lower() in password.lower():
        problems.append("contains user name")
    return problems

COMMON = ["123456", "password", "qwerty"]
for pw in ["qwerty", "Ada2026!", "blue-river-under-stone", "PASSWORD"]:
    print(pw, password_problems(pw, "ada", COMMON))
