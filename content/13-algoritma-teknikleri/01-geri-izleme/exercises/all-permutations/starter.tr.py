def permutations(items):
    result, path, used = [], [], [False] * len(items)

    def backtrack():
        # Yol tamam mi? Degilse kullanilmamis her elemani dene.
        pass

    backtrack()
    return result


for order in permutations([1, 2, 3]):
    print(order)
print(len(permutations(list(range(7)))))
