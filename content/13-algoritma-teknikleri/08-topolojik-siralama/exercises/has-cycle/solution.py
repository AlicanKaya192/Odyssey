from collections import deque


def all_nodes(deps):
    return set(deps) | {d for needs in deps.values() for d in needs}


def has_cycle(deps):
    nodes = all_nodes(deps)
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}
    for task, needs in deps.items():
        for need in needs:
            after[need].append(task)
            waiting[task] += 1
    queue = deque(n for n in nodes if waiting[n] == 0)
    taken = 0
    while queue:
        task = queue.popleft()
        taken += 1
        for nxt in after[task]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                queue.append(nxt)
    return taken < len(nodes)


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
print(has_cycle(deps))
print(has_cycle(dict(deps, extract=["report"])))
chain = {i: [i - 1] for i in range(1, 50_000)}
print(has_cycle(chain), has_cycle({**chain, 0: [49_999]}))
