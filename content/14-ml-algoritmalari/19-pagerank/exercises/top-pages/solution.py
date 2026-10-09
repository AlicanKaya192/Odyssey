def top_pages(ranks, names, k):
    order = list(range(len(ranks)))
    order.sort(key=lambda i: (-ranks[i], i))
    return [names[i] for i in order[:k]]

names = ["home", "about", "blog", "shop"]
print(top_pages([0.1, 0.4, 0.2, 0.3], names, 2))
print(top_pages([0.25, 0.25, 0.3, 0.2], names, 3))
