Write the function `flaky_tests(runs)`. `runs` is a list of test results; each item is `[commit, test, result]`, the result is `"pass"` or `"fail"`.

A test that both passed and failed **on the same commit** is flaky (the result changed while the code was the same). Failing and passing on different commits is not flakiness: the code changed in between.

Return the names of the flaky tests, each once, in alphabetical order.

**Expected output:**

```
['test_login', 'test_report']
[]
```
