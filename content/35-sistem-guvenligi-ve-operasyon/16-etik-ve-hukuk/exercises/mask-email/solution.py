def mask_email(address):
    if "@" not in address:
        return "***"
    user, domain = address.split("@", 1)
    return user[0] + "***@" + domain

print(mask_email("ada@example.org"))
print(mask_email("bob@mail.example.org"))
print(mask_email("not-an-address"))
