def hanoi(n, source, target, spare):
    if n == 0:
        return []
    # 1) n-1 diski source'tan spare'e, 2) en buyugu source'tan target'a,
    # 3) n-1 diski spare'den target'a.
    pass


for move in hanoi(3, "A", "C", "B"):
    print(move[0], "->", move[1])
print(len(hanoi(10, "A", "C", "B")))
