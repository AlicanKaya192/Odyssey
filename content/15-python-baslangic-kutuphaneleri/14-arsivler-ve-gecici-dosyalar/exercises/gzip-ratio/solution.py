import gzip


def gzip_ratio(text):
    data = text.encode("utf-8")
    return round(len(data) / len(gzip.compress(data)), 1)

print(gzip_ratio("ok " * 1000))
print(gzip_ratio("abc"))
