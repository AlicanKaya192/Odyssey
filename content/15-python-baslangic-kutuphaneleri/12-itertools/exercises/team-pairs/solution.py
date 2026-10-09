from itertools import combinations


def team_pairs(names):
    return [f"{a}-{b}" for a, b in combinations(sorted(names), 2)]

for team in team_pairs(["Grace", "Ada", "Alan"]):
    print(team)
