def stack_vs_single(channels, n):
    field = 2 * n + 1
    stack = n * (channels * channels * 9 + channels)
    single = channels * channels * field * field + channels
    return [stack, single, field]

print(stack_vs_single(64, 2))
print(stack_vs_single(32, 3))
