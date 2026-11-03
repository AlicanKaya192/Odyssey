import hashlib
import hmac


def pseudonym(value, key):
    clean = value.strip().lower()
    return hmac.new(key.encode(), clean.encode(), hashlib.sha256).hexdigest()[:12]

print(pseudonym("ada@example.org", "vault-key"))
print(pseudonym("  Ada@Example.org ", "vault-key"))
print(pseudonym("ada@example.org", "other-key"))
