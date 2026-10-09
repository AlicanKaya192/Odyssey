def apply_updates(n, updates):
    diff = [0] * (n + 1)
    for lo, hi, amount in updates:
        diff[lo] += amount
        diff[hi + 1] -= amount
    result = []
    running = 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result


print(apply_updates(6, [[0, 2, 5], [1, 4, 3], [3, 5, -1]]))
print(apply_updates(3, []))
