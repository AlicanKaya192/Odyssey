from ab_data import make_checkout_test

test = make_checkout_test(n=3000, seed=141)
rates = test.groupby("group")["bought"].mean()
pa, pb = rates["A"], rates["B"]
print(round(pa, 4), round(pb, 4))
print(round(pb - pa, 4))
print(round(pb / pa, 3))
