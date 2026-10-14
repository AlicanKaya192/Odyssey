from tiny_chat import ask, CAPITALS


def audit(countries):
    correct = wrong = other = 0
    for country in countries:
        words = ask(country)[0].split()
        asked_about, capital = words[3], words[5]
        if capital == CAPITALS[country]:
            correct += 1
        elif asked_about != country:
            other += 1
        else:
            wrong += 1
    return [correct, wrong, other]


print(audit(["france", "turkey", "japan", "chile"]))
