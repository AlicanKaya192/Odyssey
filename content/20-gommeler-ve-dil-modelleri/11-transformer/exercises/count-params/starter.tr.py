def count_params(d, layers, vocab, ffn=4):
    return 0

print(count_params(16, 1, 6))
print(count_params(768, 12, 50000))
print(count_params(768, 12, 50000, ffn=2))
