import statistics
from ml_data import make_customers, NUMERIC


def mean_shift(reference, rows, column):
    # None olmayan degerleri topla, ortalama farkini standart sapmaya bol.
    pass


reference = make_customers(1000)
later = make_customers(1000, seed=21, month=3)
for column in NUMERIC:
    shift = mean_shift(reference, later, column)
    print(column, shift, "CHECK" if shift > 0.5 else "ok")
