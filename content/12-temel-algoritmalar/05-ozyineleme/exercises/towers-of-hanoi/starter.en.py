def hanoi(n, source, target, spare):
    if n == 0:
        return []
    # 1) n-1 discs from source to spare, 2) the largest from source to target,
    # 3) n-1 discs from spare to target.
    pass


for move in hanoi(3, "A", "C", "B"):
    print(move[0], "->", move[1])
print(len(hanoi(10, "A", "C", "B")))
