from ab_data import make_user_log

users = make_user_log(n=8000, seed=713)
# Find the buying rate by platform (groupby). Print, one per line:
# desktop, mobile and their difference (desktop - mobile), 4 places.
