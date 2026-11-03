from ab_data import make_segment_test

test = make_segment_test(seed=33)
# For each platform (groupby("platform")) print the platform's name, the
# relative lift (B / A - 1, 3 places) and the number of users on one line.
