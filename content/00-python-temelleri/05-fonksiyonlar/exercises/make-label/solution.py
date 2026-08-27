def make_label(text, prefix="INFO"):
    return prefix + ": " + text


first = make_label("Server started")
second = make_label("Disk almost full", "WARN")

print(first)
print(second)
