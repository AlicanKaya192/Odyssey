def build_graph(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def most_connected(edges):
    graph = build_graph(edges)
    # By degree descending, by name on a tie.
    pass


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"]]
print(most_connected(edges))
print(most_connected([["x", "y"], ["y", "z"], ["a", "y"]]))
