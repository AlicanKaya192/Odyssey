def guess_odds(bits):
    return f"1 in {2 ** bits:,}"


def average_tries(bits):
    return 2 ** (bits - 1)

for bits in [8, 16, 28]:
    print(f"{bits}: {guess_odds(bits)}")
    print(f"  average {average_tries(bits)}")
