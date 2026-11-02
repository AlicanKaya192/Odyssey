import hashlib


def bucket(user_id, salt):
    text = f"{salt}:{user_id}"
    return sum(ord(c) for c in text) % 100


print(bucket("U00001", "checkout-v2"))
print(bucket("U00002", "checkout-v2"))
