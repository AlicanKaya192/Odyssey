import string


def substitute(text, key):
    table = str.maketrans(string.ascii_lowercase, key)
    return text.translate(table)

key = "qwertyuiopasdfghjklzxcvbnm"
print(substitute("attack at dawn", key))
print(substitute("Hello World", key))
