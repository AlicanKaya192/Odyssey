from ml_data import make_customers


def infer_schema(rows, numeric, categorical, margin):
    # Sayisal sutunlara payli aralik, kategoriklere sirali deger listesi.
    pass


schema = infer_schema(make_customers(2000), ["monthly_fee", "usage_hours"], ["plan"], 0.1)
for column, rule in schema.items():
    print(column, rule)
