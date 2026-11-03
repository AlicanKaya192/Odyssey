import hashlib
import hmac


def share_record(record, allowed, key):
    result = {k: v for k, v in record.items() if k in allowed}
    if "email" in result:
        clean = result["email"].strip().lower()
        digest = hmac.new(key.encode(), clean.encode(), hashlib.sha256)
        result["email"] = digest.hexdigest()[:12]
    return result

RECORD = {"name": "Ada", "email": " Ada@Example.org",
          "phone": "555-0100", "plan": "pro"}
shared = share_record(RECORD, ["email", "plan"], "vault-key")
for key in sorted(shared):
    print(key, shared[key])
