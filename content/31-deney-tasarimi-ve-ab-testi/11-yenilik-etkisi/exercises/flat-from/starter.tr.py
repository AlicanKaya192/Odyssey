def flat_from(weekly_lifts, tol=0.01):
    for k in range(1, len(weekly_lifts)):
        if abs(weekly_lifts[k] - weekly_lifts[k - 1]) < tol:
            return k
    return 0


print(flat_from([0.136, 0.066, 0.048, 0.052]))
print(flat_from([0.2, 0.1, 0.05]))
