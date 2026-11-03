from ab_data import make_novelty_test

clicks = make_novelty_test(n=10000, seed=12)
clicks["week"] = (clicks["day"] - 1) // 7 + 1
# For existing (is_new False) and new (True) users print the weekly
# relative lifts (B / A - 1, 3 places) as a list: the group's value
# (False / True) first, then the list.
