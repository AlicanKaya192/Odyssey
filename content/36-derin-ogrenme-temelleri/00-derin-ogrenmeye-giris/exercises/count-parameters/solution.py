def count_parameters(sizes):
    total = 0
    for n_in, n_out in zip(sizes, sizes[1:]):
        total += n_in * n_out + n_out
    return total

print(count_parameters([64, 32, 10]))
print(count_parameters([4, 8, 8, 3]))
