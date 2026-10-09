import zlib


def hash_buckets(text, buckets):
    vector = [0] * buckets
    for word in text.lower().split():
        vector[zlib.crc32(word.encode()) % buckets] += 1
    return vector

print(hash_buckets("the cat sat on the mat", 8))
print(hash_buckets("data data data", 4))
