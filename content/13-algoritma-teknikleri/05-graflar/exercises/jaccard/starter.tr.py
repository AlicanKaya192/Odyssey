def build_graph(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def jaccard(edges, a, b):
    graph = build_graph(edges)
    first, second = graph.get(a, set()), graph.get(b, set())
    # Kesisim / birlesim.
    return 0.0


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"]]
print(jaccard(edges, "ada", "deniz"))
print(jaccard(edges, "bora", "cem"))
print(jaccard(edges, "ada", "fuat"))
