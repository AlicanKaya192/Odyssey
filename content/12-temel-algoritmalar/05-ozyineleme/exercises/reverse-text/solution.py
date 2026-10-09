def reverse_text(text):
    if text == "":
        return ""
    return reverse_text(text[1:]) + text[0]


print(reverse_text("python"))
print(reverse_text("a"))
print(reverse_text("level"))
