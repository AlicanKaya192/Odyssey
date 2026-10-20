def decide(score, threshold, customer):
    # Once modelin calisip calismadigina bak.
    pass


customer = {"support_calls": 3}
print(decide(0.42, 0.31, customer))
print(decide(0.12, 0.31, customer))
print(decide(None, 0.31, customer))
print(decide(None, 0.31, {"support_calls": 1}))
