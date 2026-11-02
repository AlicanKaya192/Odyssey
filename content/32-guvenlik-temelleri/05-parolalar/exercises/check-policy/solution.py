def check_policy(password, username, common):
    problems = []
    if len(password) < 12:
        problems.append("too-short")
    if password.lower() in [c.lower() for c in common]:
        problems.append("common")
    if username and username.lower() in password.lower():
        problems.append("has-username")
    return problems

common = ["123456", "Password", "qwerty", "letmein"]
print(check_policy("qwerty", "ada", common))
print(check_policy("ada-likes-long-walks", "Ada", common))
print(check_policy("lamp-river-cloud-tiger", "ada", common))
