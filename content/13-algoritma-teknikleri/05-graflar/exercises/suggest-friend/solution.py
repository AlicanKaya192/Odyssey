def build_graph(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def suggest(edges, person):
    graph = build_graph(edges)
    scores = {}
    for friend in graph[person]:
        for other in graph[friend]:
            if other != person and other not in graph[person]:
                scores[other] = scores.get(other, 0) + 1
    if not scores:
        return None
    return min(scores, key=lambda n: (-scores[n], n))


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"]]
for person in ["ada", "ece", "fuat", "cem"]:
    print(person, "->", suggest(edges, person))
