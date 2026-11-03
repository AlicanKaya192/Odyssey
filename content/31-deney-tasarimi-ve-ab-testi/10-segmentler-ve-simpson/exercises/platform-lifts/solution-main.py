from ab_data import make_segment_test

test = make_segment_test(seed=33)
for name, part in test.groupby("platform"):
    rates = part.groupby("group")["bought"].mean()
    print(name, round(float(rates["B"] / rates["A"] - 1), 3), len(part))
