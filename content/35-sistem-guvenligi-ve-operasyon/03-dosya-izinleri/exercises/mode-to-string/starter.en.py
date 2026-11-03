def mode_to_string(mode):
    letters = ""
    # owner, group, others: shift 6, 3, 0
    return letters

for mode in [0o755, 0o640, 0o600, 0o7]:
    print(oct(mode), mode_to_string(mode))
