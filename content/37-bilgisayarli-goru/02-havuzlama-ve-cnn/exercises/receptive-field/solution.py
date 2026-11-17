def receptive_field(layers):
    field, jump = 1, 1
    for k, s in layers:
        field += (k - 1) * jump
        jump *= s
    return field

print(receptive_field([[3, 1], [3, 1]]))
print(receptive_field([[3, 1], [2, 2], [3, 1], [2, 2], [3, 1]]))
print(receptive_field([[7, 2], [3, 2], [3, 1]]))
