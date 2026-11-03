from collections import deque


def reachable(links, start):
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in links.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen - {start})

links = {"laptop": ["web"], "web": ["hr-db"], "backup": ["hr-db"],
         "hr-db": []}
print(reachable(links, "laptop"))
print(reachable(links, "backup"))
print(reachable(links, "hr-db"))
