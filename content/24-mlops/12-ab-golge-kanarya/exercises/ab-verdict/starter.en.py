def ab_verdict(diff, aa_gaps):
    # Find the band, interpret the difference against it.
    pass


gaps = [0.005 * i for i in range(20)]
print(ab_verdict(0.136, gaps))
print(ab_verdict(-0.05, gaps))
print(ab_verdict(0.2, gaps))
