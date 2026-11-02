from ab_data import make_population

users = make_population()
print(len(users))
print(round(users["minutes"].mean(), 2))
print(round(users["bought"].mean(), 3))
