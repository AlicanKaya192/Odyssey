def allowed(role, operation, policy):
    return operation in policy[role]

POLICY = {
    "everyone": ["open_window"],
    "user": ["read_own_file"],
    "admin": ["read_own_file", "install_driver"],
}
print(allowed("user", "read_own_file", POLICY))
print(allowed("user", "install_driver", POLICY))
print(allowed("guest", "open_window", POLICY))
print(allowed("guest", "read_own_file", POLICY))
