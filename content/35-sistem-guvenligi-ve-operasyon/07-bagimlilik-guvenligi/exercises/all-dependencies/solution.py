def all_dependencies(graph, root):
    seen = set()
    stack = list(graph.get(root, []))
    while stack:
        name = stack.pop()
        if name == root or name in seen:
            continue
        seen.add(name)
        stack.extend(graph.get(name, []))
    return sorted(seen)

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
