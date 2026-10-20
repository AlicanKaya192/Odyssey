import statistics
from ml_data import make_customers, NUMERIC


def mean_shift(reference, rows, column):
    old = [row[column] for row in reference if row[column] is not None]
    new = [row[column] for row in rows if row[column] is not None]
    distance = abs(statistics.mean(new) - statistics.mean(old))
    return round(distance / statistics.pstdev(old), 2)


reference = make_customers(1000)
later = make_customers(1000, seed=21, month=3)
for column in NUMERIC:
    shift = mean_shift(reference, later, column)
    print(column, shift, "CHECK" if shift > 0.5 else "ok")
