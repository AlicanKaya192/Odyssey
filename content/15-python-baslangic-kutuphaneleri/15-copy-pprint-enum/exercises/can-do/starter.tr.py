from enum import Flag, auto


class Perm(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


def combine(names):
    result = Perm(0)
    for name in names:
        result |= Perm[name]
    return result


def can_do(granted, needed):
    # combine(needed) in combine(granted)
    return False

print(can_do(["READ", "WRITE"], ["WRITE"]))
print(can_do(["READ"], ["READ", "EXECUTE"]))
