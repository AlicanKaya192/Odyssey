from ml_data import make_customers


def infer_schema(rows, numeric, categorical, margin):
    schema = {}
    for column in numeric:
        values = [row[column] for row in rows]
        low, high = min(values), max(values)
        extra = margin * (high - low)
        schema[column] = {"min": round(max(0.0, low - extra), 2), "max": round(high + extra, 2)}
    for column in categorical:
        schema[column] = {"allowed": sorted(set(row[column] for row in rows))}
    return schema


schema = infer_schema(make_customers(2000), ["monthly_fee", "usage_hours"], ["plan"], 0.1)
for column, rule in schema.items():
    print(column, rule)
