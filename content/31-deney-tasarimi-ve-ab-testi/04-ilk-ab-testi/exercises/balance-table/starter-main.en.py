from ab_data import make_experiment

test = make_experiment(n=12000, seed=741)
test["mobile"] = (test["platform"] == "mobile").astype(int)
# Find the means of sessions and mobile by group (groupby).
# On the first line print A's and B's mean sessions, on the second their
# mobile shares, with 3 places.
