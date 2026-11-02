from ab_data import make_user_log

users = make_user_log(n=8000, seed=712)
print(round(users["refunded"].mean(), 4))
print(round(users["refunded"].mean(), 4))
