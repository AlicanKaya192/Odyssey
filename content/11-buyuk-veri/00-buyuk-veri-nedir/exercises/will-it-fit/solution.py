def max_rows(ram_gb, columns):
    usable = ram_gb * 1024**3 // 2
    row_bytes = columns * 8
    return usable // row_bytes
