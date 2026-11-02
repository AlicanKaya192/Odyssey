import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


print(bucket("U00001", "checkout-v2"))
print(bucket("U00002", "checkout-v2"))
