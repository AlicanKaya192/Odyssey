from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, text):
        self.text = text
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts


def sort_versions(texts):
    return [v.text for v in sorted(Version(t) for t in texts)]

print(sort_versions(["1.10", "1.2", "1.2.1", "0.9"]))
print(Version("2.0") >= Version("1.10"))
