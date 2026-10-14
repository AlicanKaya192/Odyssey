def unknown_needs(needs):
    # For every job, check whether the names it waits for are in the dictionary.
    pass


jobs = {
    "lint": [],
    "test": [],
    "build": ["lint", "tests"],
    "deploy": ["build", "approve"],
}
print(unknown_needs(jobs))
print(unknown_needs({"a": [], "b": ["a"]}))
