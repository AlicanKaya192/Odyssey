from collections import deque


def all_nodes(deps):
    return set(deps) | {d for needs in deps.values() for d in needs}


def has_cycle(deps):
    nodes = all_nodes(deps)
    # Kahn: kac is siraya girebiliyor?
    return False


deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}
print(has_cycle(deps))
print(has_cycle(dict(deps, extract=["report"])))
chain = {i: [i - 1] for i in range(1, 50_000)}
print(has_cycle(chain), has_cycle({**chain, 0: [49_999]}))
