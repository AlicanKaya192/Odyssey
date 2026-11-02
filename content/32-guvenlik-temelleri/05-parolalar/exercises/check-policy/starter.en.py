def check_policy(password, username, common):
    problems = []
    # check the three rules in order
    return problems

common = ["123456", "Password", "qwerty", "letmein"]
print(check_policy("qwerty", "ada", common))
print(check_policy("ada-likes-long-walks", "Ada", common))
print(check_policy("lamp-river-cloud-tiger", "ada", common))
