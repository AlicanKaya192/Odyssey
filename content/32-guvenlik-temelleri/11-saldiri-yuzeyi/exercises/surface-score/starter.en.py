WEIGHT = {"internet": 3, "internal": 2, "local": 1}


def entry_score(exposure, auth):
    weight = WEIGHT.get(exposure, 3)
    return weight * (1 if auth else 2)


def surface_score(points):
    # add up every point's score
    return 0

points = [
    {"name": "login", "exposure": "internet", "auth": True},
    {"name": "search", "exposure": "internet", "auth": False},
    {"name": "admin", "exposure": "internal", "auth": True},
]
print(surface_score(points))
print(surface_score([]))
