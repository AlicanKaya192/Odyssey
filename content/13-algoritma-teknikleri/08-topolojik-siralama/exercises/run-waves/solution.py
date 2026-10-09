def all_nodes(deps):
    return set(deps) | {d for needs in deps.values() for d in needs}


def waves(deps):
    nodes = all_nodes(deps)
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}
    for task, needs in deps.items():
        for need in needs:
            after[need].append(task)
            waiting[task] += 1
    current = sorted(n for n in nodes if waiting[n] == 0)
    result = []
    while current:
        result.append(current)
        nxt = []
        for task in current:
            for later in after[task]:
                waiting[later] -= 1
                if waiting[later] == 0:
                    nxt.append(later)
        current = sorted(nxt)
    return result


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
for wave in waves(deps):
    print(wave)
