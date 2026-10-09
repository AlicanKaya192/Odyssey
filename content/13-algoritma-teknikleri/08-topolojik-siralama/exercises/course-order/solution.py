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


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
for task in course_order(deps):
    print(task)
print(course_order(dict(deps, extract=["report"])))
