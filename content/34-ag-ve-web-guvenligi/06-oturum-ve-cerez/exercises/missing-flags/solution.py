def missing_flags(header):
    parts = [p.strip() for p in header.split(";")]
    present = {p.partition("=")[0].strip().lower() for p in parts[1:]}
    return [flag for flag in ["HttpOnly", "SameSite", "Secure"]
            if flag.lower() not in present]

for header in ["session=abc; Path=/",
               "session=abc; secure; httponly",
               "session=abc; Secure; HttpOnly; SameSite=Strict"]:
    print(missing_flags(header))
