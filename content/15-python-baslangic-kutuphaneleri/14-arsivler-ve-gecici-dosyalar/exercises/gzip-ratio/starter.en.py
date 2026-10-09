import gzip


def gzip_ratio(text):
    data = text.encode("utf-8")
    # len(data) / len(gzip.compress(data))
    return 0.0

print(gzip_ratio("ok " * 1000))
print(gzip_ratio("abc"))
