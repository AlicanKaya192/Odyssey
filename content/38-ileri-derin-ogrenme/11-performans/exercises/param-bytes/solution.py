def param_bytes(sizes, bytes_per_value):
    params = sum(a * b + b for a, b in zip(sizes, sizes[1:]))
    return params * bytes_per_value

print(param_bytes([64, 128, 10], 4))
print(param_bytes([64, 128, 10], 2))
