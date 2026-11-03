def missing_flags(header):
    # ; ile bol, ilk parca ad=deger; gerisinin adlarini kucuk harfle topla
    return []

for header in ["session=abc; Path=/",
               "session=abc; secure; httponly",
               "session=abc; Secure; HttpOnly; SameSite=Strict"]:
    print(missing_flags(header))
