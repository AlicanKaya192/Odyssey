import statistics as st


def describe(values):
    return (st.mean(values), st.median(values),
            round(st.stdev(values), 2), round(st.pstdev(values), 2))

print(describe([2, 4, 4, 4, 5, 5, 7, 9]))
