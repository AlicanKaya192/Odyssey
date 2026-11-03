import hashlib
import hmac


def share_record(record, allowed, key):
    result = {k: v for k, v in record.items() if k in allowed}
    if "email" in result:
        result["email"] = hashlib.sha256(result["email"].encode()).hexdigest()[:12]
    return result

RECORD = {"name": "Ada", "email": " Ada@Example.org",
          "phone": "555-0100", "plan": "pro"}
shared = share_record(RECORD, ["email", "plan"], "vault-key")
for key in sorted(shared):
    print(key, shared[key])
