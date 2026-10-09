def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] >= heap[parent]:
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def pop(heap):
    last = heap.pop()
    if not heap:
        return last
    top, heap[0] = heap[0], last
    i = 0
    # Kucuk cocukla yer degistirerek in.

    return top


def pop_all(values):
    heap = []
    for x in values:
        push(heap, x)
    return [pop(heap) for _ in range(len(values))]


print(pop_all([5, 3, 8, 1, 9, 2]))
print(pop_all([4, 4, 1, 7]))
