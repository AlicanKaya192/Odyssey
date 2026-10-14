def best_threshold(scores, target, grid):
    def share(t):
        return sum(s >= t for s in scores) / len(scores)
    return min(grid, key=lambda t: abs(share(t) - target))


print(best_threshold([0.9, 0.6, 0.4, 0.3, 0.2], 0.6, [0.2, 0.3, 0.4, 0.5]))
