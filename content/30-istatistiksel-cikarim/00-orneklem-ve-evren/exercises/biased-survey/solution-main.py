from ab_data import make_population

users = make_population()
heavy = users[users["visits"] >= 5]
print(round(len(heavy) / len(users), 3))
print(round(users["minutes"].mean(), 2))
print(round(heavy["minutes"].mean(), 2))
gap = heavy["minutes"].mean() - users["minutes"].mean()
print(round(gap, 2))
