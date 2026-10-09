import shelve


def add_scores(path, pairs):
    with shelve.open(path) as db:
        for name, score in pairs:
            if name not in db:
                db[name] = []
            db[name].append(score)
        return {name: db[name] for name in sorted(db)}

print(add_scores("scores", [["ada", 90], ["alan", 75], ["ada", 85]]))
