def public_status(found, allowed, logged_in):
    if not found:
        return 404
    if not allowed:
        return 403
    return 200

print(public_status(True, True, False))
print(public_status(True, True, True))
print(public_status(True, False, True))
print(public_status(False, False, True))
