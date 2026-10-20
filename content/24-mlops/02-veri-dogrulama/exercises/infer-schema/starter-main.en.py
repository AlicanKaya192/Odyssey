from ml_data import make_customers


def infer_schema(rows, numeric, categorical, margin):
    # A range with a margin for numeric columns, a sorted list of values for categorical ones.
    pass


schema = infer_schema(make_customers(2000), ["monthly_fee", "usage_hours"], ["plan"], 0.1)
for column, rule in schema.items():
    print(column, rule)
