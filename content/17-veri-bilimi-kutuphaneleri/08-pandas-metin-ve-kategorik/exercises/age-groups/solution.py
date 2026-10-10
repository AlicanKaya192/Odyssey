import pandas as pd


def age_groups(ages):
    labels = ["child", "young", "middle", "senior"]
    groups = pd.cut(pd.Series(ages), bins=[0, 18, 40, 65, 120], labels=labels)
    return groups.value_counts(sort=False).to_dict()

print(*age_groups([15, 22, 37, 70, 8]).items(), sep="\n")
