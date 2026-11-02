import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


def assign(user_id, salt, share_b=50):
    return "B" if bucket(user_id, salt) > share_b else "A"


print(assign("U00001", "checkout-v2"))
print(assign("U00007", "checkout-v2", share_b=10))
