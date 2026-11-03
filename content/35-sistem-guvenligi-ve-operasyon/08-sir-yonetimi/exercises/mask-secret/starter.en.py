def mask(value):
    return "****" + value[-4:]

print(mask("sk-live-9f3a1a2b"))
print(mask("abcd"))
print(mask(""))
