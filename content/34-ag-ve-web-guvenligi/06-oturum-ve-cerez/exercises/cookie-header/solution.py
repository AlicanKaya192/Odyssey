def cookie_header(name, value, max_age):
    parts = [f"{name}={value}", f"Max-Age={max_age}", "Path=/",
             "Secure", "HttpOnly", "SameSite=Lax"]
    return "; ".join(parts)

for part in cookie_header("session", "abc123", 3600).split("; "):
    print(part)
