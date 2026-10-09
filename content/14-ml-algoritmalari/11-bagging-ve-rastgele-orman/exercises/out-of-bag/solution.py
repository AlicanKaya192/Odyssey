def out_of_bag(n, bag):
    seen = set(bag)
    return [i for i in range(n) if i not in seen]

print(out_of_bag(6, [0, 0, 2, 3, 3, 5]))
