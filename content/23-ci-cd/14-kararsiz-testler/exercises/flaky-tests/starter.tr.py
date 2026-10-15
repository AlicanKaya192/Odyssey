def flaky_tests(runs):
    # (commit, test) ciftine gore gorulen sonuclari bir kumede topla.
    pass


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
