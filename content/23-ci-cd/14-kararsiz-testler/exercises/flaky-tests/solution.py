def flaky_tests(runs):
    results = {}
    for commit, test, result in runs:
        results.setdefault((commit, test), set()).add(result)
    flaky = set()
    for (commit, test), seen in results.items():
        if "pass" in seen and "fail" in seen:
            flaky.add(test)
    return sorted(flaky)


runs = [
    ["a1f", "test_login", "pass"],
    ["a1f", "test_cart", "pass"],
    ["a1f", "test_login", "fail"],
    ["b2e", "test_cart", "fail"],
    ["b2e", "test_report", "pass"],
    ["c3d", "test_cart", "pass"],
    ["b2e", "test_report", "fail"],
]
print(flaky_tests(runs))
print(flaky_tests(runs[:2]))
