import heapq


def run_order(tasks):
    heap = []
    for number, (priority, name) in enumerate(tasks):
        heapq.heappush(heap, (priority, number, name))
    order = []
    while heap:
        order.append(heapq.heappop(heap)[2])
    return order


tasks = [[2, "tests"], [1, "bugfix"], [3, "docs"], [1, "deploy"], [2, "review"]]
for name in run_order(tasks):
    print(name)
