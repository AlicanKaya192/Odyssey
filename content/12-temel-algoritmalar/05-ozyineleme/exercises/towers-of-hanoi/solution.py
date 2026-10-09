def hanoi(n, source, target, spare):
    if n == 0:
        return []
    moves = hanoi(n - 1, source, spare, target)
    moves.append((source, target))
    moves += hanoi(n - 1, spare, target, source)
    return moves


for move in hanoi(3, "A", "C", "B"):
    print(move[0], "->", move[1])
print(len(hanoi(10, "A", "C", "B")))
