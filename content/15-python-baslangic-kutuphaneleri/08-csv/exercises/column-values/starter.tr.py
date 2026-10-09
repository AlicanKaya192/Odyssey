def column_values(path, column):
    values = []
    with open(path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        index = header.index(column)
        for line in f:
            values.append(line.strip().split(",")[index])
    return values

for city in column_values("sales.csv", "city"):
    print(city)
