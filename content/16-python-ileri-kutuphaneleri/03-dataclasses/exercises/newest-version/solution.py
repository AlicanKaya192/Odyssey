from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int


def newest(texts):
    versions = [Version(*map(int, t.split("."))) for t in texts]
    best = max(versions)
    return f"{best.major}.{best.minor}.{best.patch}"

print(newest(["1.2.0", "1.10.0", "1.9.9"]))
print(newest(["0.1.0"]))
