def cookie_problems(header):
    parts = header.split(";")[1:]
    names = {part.split("=")[0].strip().lower() for part in parts}
    missing = []
    for flag in ["Secure", "HttpOnly", "SameSite"]:
        if flag.lower() not in names:
            missing.append(flag)
    return missing

for header in [
    "sid=abc; Path=/; Secure; HttpOnly; SameSite=Lax",
    "sid=abc; Path=/; HttpOnly",
    "secure=1; Path=/",
    "sid=abc; SECURE; httponly; samesite=Strict",
]:
    print(cookie_problems(header))
