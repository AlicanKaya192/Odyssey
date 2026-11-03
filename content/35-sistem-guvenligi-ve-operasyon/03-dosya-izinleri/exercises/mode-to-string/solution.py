def mode_to_string(mode):
    letters = ""
    for shift in (6, 3, 0):
        bits = (mode >> shift) & 7
        letters += "r" if bits & 4 else "-"
        letters += "w" if bits & 2 else "-"
        letters += "x" if bits & 1 else "-"
    return letters

for mode in [0o755, 0o640, 0o600, 0o7]:
    print(oct(mode), mode_to_string(mode))
