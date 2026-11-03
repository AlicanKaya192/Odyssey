def canonical_email(email):
    # once kanonik bicim, sonra dogrulama
    return email

for email in ["  Ada@Example.COM ", "a@b@c.example", "@example.com", "ada"]:
    print(repr(canonical_email(email)))
