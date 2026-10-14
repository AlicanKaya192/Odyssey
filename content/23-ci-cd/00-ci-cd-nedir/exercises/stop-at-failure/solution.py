def run_pipeline(stages):
    for name, passed in stages:
        if not passed:
            return name
    return "passed"


print(run_pipeline([("install", True), ("lint", True), ("test", False), ("package", True)]))
print(run_pipeline([("install", True), ("test", True), ("package", True)]))
print(run_pipeline([("install", False), ("test", False)]))
