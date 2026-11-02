def unused_permissions(granted, used):
    return sorted(set(granted) - set(used))

granted = ["crm:read", "crm:write", "invoices:read", "payments:approve"]
used = ["invoices:read", "crm:read", "payments:approve"]
print(unused_permissions(granted, used))
print(unused_permissions(["a"], []))
