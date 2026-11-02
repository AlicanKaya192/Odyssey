WEIGHT = {"internet": 3, "internal": 2, "local": 1}


def entry_score(exposure, auth):
    return WEIGHT[exposure] * (1 if auth else 2)

print(entry_score("internet", True))
print(entry_score("internet", False))
print(entry_score("local", False))
print(entry_score("partner", True))
