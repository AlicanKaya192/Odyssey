import pandas as pd


def scores_long(table):
    wide = pd.DataFrame(table)
    return wide.values.tolist()

TABLE = {"id": [1, 2], "score_2024": [60, 75], "score_2025": [70, 80]}
print(*scores_long(TABLE), sep="\n")
