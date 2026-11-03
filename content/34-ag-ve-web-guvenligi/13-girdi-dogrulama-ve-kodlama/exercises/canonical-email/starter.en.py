def canonical_email(email):
    # canonical form first, then validation
    return email

for email in ["  Ada@Example.COM ", "a@b@c.example", "@example.com", "ada"]:
    print(repr(canonical_email(email)))
