def all_dependencies(graph, root):
    result = []
    for name in graph.get(root, []):
        result.append(name)
        result.extend(all_dependencies(graph, name))
    return result

GRAPH = {
    "app": ["web", "db"],
    "web": ["templates", "http"],
    "db": ["http", "pool"],
    "templates": ["escape", "web"],
    "http": [],
    "pool": [],
    "escape": [],
}
print(", ".join(all_dependencies(GRAPH, "app")))
print(", ".join(all_dependencies(GRAPH, "db")))
