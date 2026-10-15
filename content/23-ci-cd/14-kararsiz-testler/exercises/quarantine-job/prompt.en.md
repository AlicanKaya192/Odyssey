A test in `tests/test_shop.py` is marked with `@pytest.mark.flaky`. Separate it from the main pipeline:

- The `test` job should leave out the marked tests: `python -m pytest -q -m "not flaky"`.
- A new `quarantine` job (`ubuntu-latest`) should get the code, install the packages and run only the marked tests: `python -m pytest -q -m flaky`.
- The run should not turn red even if `quarantine` fails: `continue-on-error: true`.
