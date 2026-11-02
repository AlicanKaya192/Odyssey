import string


def substitute(text, key):
    plain = string.ascii_lowercase + string.ascii_uppercase
    table = str.maketrans(plain, key + key.upper())
    return text.translate(table)

key = "qwertyuiopasdfghjklzxcvbnm"
print(substitute("attack at dawn", key))
print(substitute("Hello World", key))
