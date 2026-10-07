import zlib


def partition(key, reducers):
    return zlib.crc32(key.encode()) % reducers
