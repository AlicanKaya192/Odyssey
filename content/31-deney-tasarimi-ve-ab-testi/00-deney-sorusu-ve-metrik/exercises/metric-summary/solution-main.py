from ab_data import make_user_log

users = make_user_log(n=5000, seed=711)
print(round(users["bought"].mean(), 4))
print(round(users["revenue"].mean(), 2))
print(round(users["minutes"].mean(), 1))
