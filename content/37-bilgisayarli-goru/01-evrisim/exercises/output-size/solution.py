def output_size(h, k, stride, padding):
    return (h + 2 * padding - k) // stride + 1

for h, k, s, p in [(16, 3, 1, 0), (16, 3, 1, 1), (16, 3, 2, 1), (32, 5, 2, 0)]:
    print(h, k, s, p, output_size(h, k, s, p))
