def common_elements(a, b):
    # b'yi kumeye cevir, a'nin elemanlarina orada bak.
    pass


print(common_elements([1, 2, 2, 3], [2, 3, 4]))
evens = list(range(0, 200_000, 2))
threes = list(range(0, 200_000, 3))
print(len(common_elements(evens, threes)))
