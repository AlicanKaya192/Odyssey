def subsets(items):
    result, path = [], []

    def backtrack(start):
        # Simdiki yolu ekle (kopya!), sonra sec - devam et - geri al.
        pass

    backtrack(0)
    return result


for subset in subsets([1, 2, 3]):
    print(subset)
print(len(subsets(list(range(10)))))
