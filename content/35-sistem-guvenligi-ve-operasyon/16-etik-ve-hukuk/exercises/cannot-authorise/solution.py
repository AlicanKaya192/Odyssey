def cannot_authorise(owners, signed_by, targets):
    found = []
    for target in targets:
        if owners.get(target) != signed_by:
            found.append(target)
    return sorted(found)

OWNERS = {"shop.example.org": "Eve", "mail.example.org": "Bob"}
TARGETS = ["shop.example.org", "mail.example.org", "vpn.example.org"]
print(cannot_authorise(OWNERS, "Bob", TARGETS))
