def vector(row, spec):
    # Collect the values in spec order; is_pro is special.
    pass


SPEC = ["tenure", "monthly_fee", "support_calls", "usage_hours", "is_pro"]
row = {"plan": "pro", "usage_hours": 5.0, "tenure": 2, "support_calls": 6, "monthly_fee": 45.0}
print(vector(row, SPEC))
print(vector({**row, "plan": "basic"}, ["is_pro", "tenure"]))
