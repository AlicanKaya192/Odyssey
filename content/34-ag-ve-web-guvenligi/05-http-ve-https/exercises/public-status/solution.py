def public_status(found, allowed, logged_in):
    if not logged_in:
        return 401
    if not found or not allowed:
        return 404
    return 200

print(public_status(True, True, False))
print(public_status(True, True, True))
print(public_status(True, False, True))
print(public_status(False, False, True))
