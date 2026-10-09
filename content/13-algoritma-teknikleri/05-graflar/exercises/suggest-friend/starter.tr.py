def build_graph(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def suggest(edges, person):
    graph = build_graph(edges)
    scores = {}
    # Arkadaslarin arkadaslarini say.
    return None


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"]]
for person in ["ada", "ece", "fuat", "cem"]:
    print(person, "->", suggest(edges, person))
