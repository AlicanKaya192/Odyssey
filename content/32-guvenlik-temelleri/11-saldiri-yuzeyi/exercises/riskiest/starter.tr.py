WEIGHT = {"internet": 3, "internal": 2, "local": 1}


def entry_score(exposure, auth):
    weight = WEIGHT.get(exposure, 3)
    return weight * (1 if auth else 2)


def riskiest(points, n):
    # puana gore sirala
    return []

points = [
    {"name": "login", "exposure": "internet", "auth": True},
    {"name": "search", "exposure": "internet", "auth": False},
    {"name": "admin", "exposure": "internal", "auth": True},
    {"name": "export", "exposure": "internal", "auth": True},
]
print(riskiest(points, 2))
print(riskiest(points, 10))
