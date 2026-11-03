def parse_version(text):
    return tuple(int(part) for part in text.split("."))


def needs_patch(installed, fixed):
    return parse_version(installed) < parse_version(fixed)

print(parse_version("2.4.10"))
print(needs_patch("2.4.9", "2.4.10"))
print(needs_patch("2.4.10", "2.4.9"))
print(needs_patch("1.10", "1.9"))
print(needs_patch("3.0", "3.0"))
