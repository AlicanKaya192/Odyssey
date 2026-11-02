from ab_data import make_user_log

users = make_user_log(n=5000, seed=711)
# Print the per-user means, one per line:
# bought (4 places), revenue (2 places), minutes (1 place).
