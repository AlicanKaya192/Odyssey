def table_mb(rows, columns):
    size = rows * columns * 8
    return round(size / 1024**2, 1)
