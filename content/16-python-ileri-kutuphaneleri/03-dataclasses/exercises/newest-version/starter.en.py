from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int
    patch: int


def newest(texts):
    return max(texts)

print(newest(["1.2.0", "1.10.0", "1.9.9"]))
print(newest(["0.1.0"]))
