from ab_data import make_population

users = make_population()
# Select only users with at least 5 visits (visits >= 5).
# 1) The group's share among users (3 places)
# 2) The mean "minutes" of all users (2 places)
# 3) The group's mean "minutes" (2 places)
# 4) The gap: group minus everyone (2 places)
