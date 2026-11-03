def can_view(user, invoice):
    # the owner or an admin?
    return True

INVOICE = {"id": 102, "owner": "bob"}
print(can_view({"name": "bob", "role": "user"}, INVOICE))
print(can_view({"name": "ada", "role": "user"}, INVOICE))
print(can_view({"name": "eve", "role": "admin"}, INVOICE))
