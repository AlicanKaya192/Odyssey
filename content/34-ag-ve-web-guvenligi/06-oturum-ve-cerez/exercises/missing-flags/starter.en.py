def missing_flags(header):
    # split on ;, the first part is name=value; collect the rest's names in lower case
    return []

for header in ["session=abc; Path=/",
               "session=abc; secure; httponly",
               "session=abc; Secure; HttpOnly; SameSite=Strict"]:
    print(missing_flags(header))
