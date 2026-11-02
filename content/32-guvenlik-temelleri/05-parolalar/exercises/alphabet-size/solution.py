def alphabet_size(password):
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(not c.isalnum() for c in password):
        size += 32
    return size

for pw in ["hello", "Hello", "Hello1", "Hello1!", "1234"]:
    print(pw, alphabet_size(pw))
