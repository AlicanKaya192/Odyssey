import hashlib
import hmac


def pseudonym(value, key):
    return hashlib.sha256(value.encode()).hexdigest()[:12]

print(pseudonym("ada@example.org", "vault-key"))
print(pseudonym("  Ada@Example.org ", "vault-key"))
print(pseudonym("ada@example.org", "other-key"))
