def all_nodes(deps):
    return set(deps) | {d for needs in deps.values() for d in needs}


def waves(deps):
    nodes = all_nodes(deps)
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}
    # Counters; then waves round by round.
    return []


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
for wave in waves(deps):
    print(wave)
