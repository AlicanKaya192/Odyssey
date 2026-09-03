records = [
    ("Ada", 62), ("Kerem", 78), ("Mina", 91), ("Deniz", 45), ("Efe", 88),
    ("Sila", 70), ("Kaan", 55), ("Ela", 83), ("Arda", 67), ("Nil", 74),
]

split = int(len(records) * 0.7)
train = records[:split]
test = records[split:]

print(len(train), len(test))
print(test[0])
print(round(sum(s for _, s in train) / len(train), 2))
