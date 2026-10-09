import heapq


def all_nodes(deps):
    return set(deps) | {d for needs in deps.values() for d in needs}


def course_order(deps):
    nodes = all_nodes(deps)
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}
    for task, needs in deps.items():
        for need in needs:
            after[need].append(task)
            waiting[task] += 1
    ready = [n for n in nodes if waiting[n] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        task = heapq.heappop(ready)
        order.append(task)
        for nxt in after[task]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                heapq.heappush(ready, nxt)
    return order if len(order) == len(nodes) else None


def finish_time(deps, hours):
    finish = {}
    # Topolojik sirayla bitisleri hesapla.
    return max(finish.values(), default=0)


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
hours = {"extract": 2, "clean": 3, "validate": 1, "features": 4,
         "train": 6, "evaluate": 1, "report": 2}
print(finish_time(deps, hours))
print(finish_time({}, {"solo": 5}))
