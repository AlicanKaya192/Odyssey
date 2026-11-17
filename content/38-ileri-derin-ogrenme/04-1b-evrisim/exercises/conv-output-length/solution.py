def conv_output_length(length, kernel, padding, stride):
    return (length + 2 * padding - kernel) // stride + 1

print(conv_output_length(64, 5, 0, 1))
print(conv_output_length(64, 5, 2, 1))
print(conv_output_length(64, 5, 0, 2))
