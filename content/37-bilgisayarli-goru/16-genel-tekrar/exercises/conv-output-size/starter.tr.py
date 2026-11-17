def conv_output_size(size, kernel, stride, padding):
    return 0

print(conv_output_size(32, 3, 1, 1))
print(conv_output_size(32, 3, 2, 1))
print(conv_output_size(28, 5, 1, 0))
