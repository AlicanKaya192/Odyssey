import shelve


def add_scores(path, pairs):
    with shelve.open(path) as db:
        for name, score in pairs:
            scores = db.get(name, [])
            scores.append(score)
            db[name] = scores
        return {name: db[name] for name in sorted(db)}

print(add_scores("scores", [["ada", 90], ["alan", 75], ["ada", 85]]))
