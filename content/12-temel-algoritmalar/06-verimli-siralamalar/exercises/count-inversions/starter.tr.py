import random


def sort_and_count(items):
    if len(items) <= 1:
        return items, 0
    # Iki yariyi say, birlestirirken sagdan alinan her eleman icin
    # soldaki kalanlarin sayisini ekle.
    pass


print(sort_and_count([2, 4, 1, 3, 5]))
print(sort_and_count([5, 4, 3, 2, 1]))
random.seed(7)
data = random.sample(range(50_000), 50_000)
print(sort_and_count(data)[1])
