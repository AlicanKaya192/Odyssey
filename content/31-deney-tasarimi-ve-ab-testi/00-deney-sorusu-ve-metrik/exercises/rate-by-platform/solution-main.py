from ab_data import make_user_log

users = make_user_log(n=8000, seed=713)
rates = users.groupby("platform")["bought"].mean()
print(round(rates["desktop"], 4))
print(round(rates["mobile"], 4))
print(round(rates["desktop"] - rates["mobile"], 4))
