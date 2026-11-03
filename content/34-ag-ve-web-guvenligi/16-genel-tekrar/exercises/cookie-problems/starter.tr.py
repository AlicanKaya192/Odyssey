def cookie_problems(header):
    missing = []
    for flag in ["Secure", "HttpOnly", "SameSite"]:
        if flag not in header:
            missing.append(flag)
    return missing

for header in [
    "sid=abc; Path=/; Secure; HttpOnly; SameSite=Lax",
    "sid=abc; Path=/; HttpOnly",
    "secure=1; Path=/",
    "sid=abc; SECURE; httponly; samesite=Strict",
]:
    print(cookie_problems(header))
