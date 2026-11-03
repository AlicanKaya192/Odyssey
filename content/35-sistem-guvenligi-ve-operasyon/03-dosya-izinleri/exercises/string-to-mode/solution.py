def string_to_mode(text):
    mode = 0
    for letter in text:
        mode = mode * 2
        if letter != "-":
            mode += 1
    return mode

for text in ["rwxr-xr-x", "rw-r-----", "rw-------", "---------"]:
    print(text, oct(string_to_mode(text)))
