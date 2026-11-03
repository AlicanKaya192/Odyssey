def guess_odds(bits):
    # the "1 in ..." text
    return ""


def average_tries(bits):
    # half the possible addresses
    return 0

for bits in [8, 16, 28]:
    print(f"{bits}: {guess_odds(bits)}")
    print(f"  average {average_tries(bits)}")
