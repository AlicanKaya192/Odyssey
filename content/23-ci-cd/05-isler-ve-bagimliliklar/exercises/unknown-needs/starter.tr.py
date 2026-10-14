def unknown_needs(needs):
    # Her isin bekledigi adlarin sozlukte olup olmadigina bak.
    pass


jobs = {
    "lint": [],
    "test": [],
    "build": ["lint", "tests"],
    "deploy": ["build", "approve"],
}
print(unknown_needs(jobs))
print(unknown_needs({"a": [], "b": ["a"]}))
