def check_policy(password, username, common):
    problems = []
    # uc kurali sirayla denetle
    return problems

common = ["123456", "Password", "qwerty", "letmein"]
print(check_policy("qwerty", "ada", common))
print(check_policy("ada-likes-long-walks", "Ada", common))
print(check_policy("lamp-river-cloud-tiger", "ada", common))
