def run_pipeline(stages):
    # Look at the stages in order; return the name of the first failing one.
    pass


print(run_pipeline([("install", True), ("lint", True), ("test", False), ("package", True)]))
print(run_pipeline([("install", True), ("test", True), ("package", True)]))
print(run_pipeline([("install", False), ("test", False)]))
