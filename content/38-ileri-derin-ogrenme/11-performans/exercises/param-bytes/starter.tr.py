def param_bytes(sizes, bytes_per_value):
    # sizes: katman boyutlari, ornek [64, 128, 10] -> Linear(64, 128), Linear(128, 10)
    return 0

print(param_bytes([64, 128, 10], 4))
print(param_bytes([64, 128, 10], 2))
