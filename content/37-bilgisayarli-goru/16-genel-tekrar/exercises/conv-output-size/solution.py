def conv_output_size(size, kernel, stride, padding):
    return (size + 2 * padding - kernel) // stride + 1

print(conv_output_size(32, 3, 1, 1))
print(conv_output_size(32, 3, 2, 1))
print(conv_output_size(28, 5, 1, 0))
