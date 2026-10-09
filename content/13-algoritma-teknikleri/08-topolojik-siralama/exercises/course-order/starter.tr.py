import heapq


def all_nodes(deps):
    return set(deps) | {d for needs in deps.values() for d in needs}


def course_order(deps):
    nodes = all_nodes(deps)
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}
    # Sayaclari kur; beklemeyenleri heap'e koy.
    return None


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
for task in course_order(deps):
    print(task)
print(course_order(dict(deps, extract=["report"])))
