def ab_verdict(diff, aa_gaps):
    ordered = sorted(aa_gaps)
    band = round(ordered[int(0.95 * len(ordered))], 3)
    if abs(diff) > band:
        return ["real", band]
    return ["noise", band]


gaps = [0.005 * i for i in range(20)]
print(ab_verdict(0.136, gaps))
print(ab_verdict(-0.05, gaps))
print(ab_verdict(0.2, gaps))
