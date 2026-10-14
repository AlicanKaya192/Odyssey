def run_pipeline(stages):
    # Asamalara sirayla bak; ilk duseni bulunca adini dondur.
    pass


print(run_pipeline([("install", True), ("lint", True), ("test", False), ("package", True)]))
print(run_pipeline([("install", True), ("test", True), ("package", True)]))
print(run_pipeline([("install", False), ("test", False)]))
