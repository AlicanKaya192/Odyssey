def split_range(n, parts):
    size = n // parts
    pieces = []
    for i in range(parts):
        start = i * size
        stop = n if i == parts - 1 else (i + 1) * size
        pieces.append((start, stop))
    return pieces
