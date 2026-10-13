def collapse_spaces(text):
    return " ".join(text.split())

print(collapse_spaces("too   many    spaces"))
print(collapse_spaces("tab\there\nand a new line"))
print(collapse_spaces("   edges   "))
