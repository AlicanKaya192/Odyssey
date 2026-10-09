import sys


def version_ok(info, minimum):
    # tuple(info[:len(minimum)]) >= tuple(minimum)
    return False

print(version_ok((3, 14, 7), (3, 10)))
print(version_ok((3, 9, 1), (3, 10)))
print(version_ok(sys.version_info, (3, 8)))
