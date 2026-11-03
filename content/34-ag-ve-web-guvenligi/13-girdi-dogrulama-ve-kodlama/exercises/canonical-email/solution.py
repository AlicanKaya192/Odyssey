def canonical_email(email):
    email = email.strip().lower()
    if email.count("@") != 1:
        return None
    local, domain = email.split("@")
    if not local or not domain:
        return None
    return email

for email in ["  Ada@Example.COM ", "a@b@c.example", "@example.com", "ada"]:
    print(repr(canonical_email(email)))
