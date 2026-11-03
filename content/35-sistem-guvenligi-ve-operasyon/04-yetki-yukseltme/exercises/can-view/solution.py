def can_view(user, invoice):
    if user["role"] == "admin":
        return True
    return invoice["owner"] == user["name"]

INVOICE = {"id": 102, "owner": "bob"}
print(can_view({"name": "bob", "role": "user"}, INVOICE))
print(can_view({"name": "ada", "role": "user"}, INVOICE))
print(can_view({"name": "eve", "role": "admin"}, INVOICE))
