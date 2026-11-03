def access(request, grants):
    allowed = grants.get(request["user"], [])
    if request["mfa"] and request["device_ok"] and request["resource"] in allowed:
        return "allow"
    return "deny"

GRANTS = {"ada": ["wiki", "hr-db"], "bob": ["wiki"]}
attempts = [
    {"user": "ada", "inside": False, "mfa": True, "device_ok": True, "resource": "hr-db"},
    {"user": "bob", "inside": True, "mfa": True, "device_ok": True, "resource": "hr-db"},
    {"user": "ada", "inside": True, "mfa": False, "device_ok": True, "resource": "wiki"},
    {"user": "eve", "inside": True, "mfa": True, "device_ok": True, "resource": "wiki"},
]
for r in attempts:
    print(r["user"], r["resource"], access(r, GRANTS))
