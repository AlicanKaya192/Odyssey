def count_params(d, layers, vocab, ffn=4):
    attention = 4 * d * d
    feed_forward = 2 * ffn * d * d
    norms = 4 * d
    return layers * (attention + feed_forward + norms) + vocab * d

print(count_params(16, 1, 6))
print(count_params(768, 12, 50000))
print(count_params(768, 12, 50000, ffn=2))
