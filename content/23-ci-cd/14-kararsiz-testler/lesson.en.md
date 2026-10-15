# Flaky Tests and Debugging

A test that passes in one run and fails in another although the code did
not change is called a **flaky test**. A flaky test is the sneakiest
problem a pipeline has: the person who sees the red cross says "that test
again" and runs it again, and one day a real bug slips through the same
way. In this section we measure where flakiness comes from, see how to
fix it and how to find the cause of a failing pipeline.

## How much harm does one flaky test do?

Say a test fails for no reason in two runs out of a hundred: it passes
98%. On its own that looks small. But for the pipeline to be green,
**all** tests must pass at the same time; as flaky tests add up, the
chances multiply:

```python
for flaky in [1, 5, 20]:
    chance = 0.98 ** flaky
    print(f"{flaky:>2} flaky tests: suite passes {chance:.0%}")
```

```text
 1 flaky tests: suite passes 98%
 5 flaky tests: suite passes 90%
20 flaky tests: suite passes 67%
```

With twenty flaky tests the pipeline is red for no reason in one run out
of three. At that point nobody believes red any more; all of CI's value
rests on the trust that "red = something broke".

## Where flakiness comes from

| Source | Example | Fix |
|---|---|---|
| Order dependence | A test relies on data the previous one left behind | Every test sets up its own data (fixture) |
| Time | `datetime.now()` gives another result at the weekend | Pass the clock in from outside |
| Randomness | `random` without a seed | A fixed seed (`random.Random(42)`) |
| Set and dict order | A text set's order changes from run to run | Fix the order with `sorted` |
| Waiting and races | `sleep(1)` "should be enough" | Wait for the condition, not for a time |
| Network | A real request to a site in a test | A fake server or a recorded answer |

Let's see three of them by measuring.

## The order of a set

Python computes the `hash` of texts with a different seed in every
process (for security). This is why the order in which a set of texts is
walked can change **from process to process**. The person who wrote the
"test" below looked at the set's order once on their own computer and
wrote it down. We run the test in ten separate processes, each with a
different seed (`PYTHONHASHSEED`):

```python
import os
import subprocess
import sys

test = 'assert list({"api", "db", "web"}) == ["db", "web", "api"]'
results = []
for seed in range(10):
    env = {**os.environ, "PYTHONHASHSEED": str(seed)}
    run = subprocess.run([sys.executable, "-c", test], env=env)
    results.append("pass" if run.returncode == 0 else "FAIL")
print(" ".join(results))
print("passed:", results.count("pass"), "of", len(results))
```

```text
pass pass FAIL FAIL pass FAIL pass FAIL FAIL FAIL
passed: 4 of 10
```

The code is the same, the result changes from run to run: it passed in
4 of the ten runs. It passing on the writer's computer
was luck. The fix: do not rely on the order. Compare with `sorted(...)`
or with the set itself (`== {"api", "db", "web"}`).

## Order dependence

Two tests share the same module variable:

```python
cart = []


def add(item):
    cart.append(item)
    return len(cart)


def test_add_first():
    assert add("apple") == 1


def test_add_second_alone():
    assert add("pear") == 1
```

The second test passes when it runs alone and fails when the whole file
runs (`--tb=no` hides the error details; a short summary stays at the
end):

```text
> python -m pytest -q --tb=no test_cart.py::test_add_second_alone
.                                                                        [100%]
1 passed

> python -m pytest -q --tb=no
.F                                                                       [100%]
=========================== short test summary info ===========================
FAILED test_cart.py::test_add_second_alone - AssertionError: assert 2 == 1
1 failed, 1 passed
```

A test that passes alone but fails with others relies on the state the
previous one left behind. Running in parallel or a plugin that changes
the test order will make it fail one day. The fix: a **fixture** that
sets up each test's own data:

```python
import pytest


@pytest.fixture
def cart():
    return []


def add(cart, item):
    cart.append(item)
    return len(cart)


def test_add_first(cart):
    assert add(cart, "apple") == 1


def test_add_second_alone(cart):
    assert add(cart, "pear") == 1
```

```text
> python -m pytest -q
..                                                                       [100%]
2 passed
```

## Time

The test of a function that calls `datetime.now()` depends on **which
day** the test runs. The pipeline's machine also runs on UTC; around
midnight it can be a different day than on your clock. The fix: pass the
clock into the function from outside. The test gives a fixed date, the
program gives none:

```python
from datetime import datetime


def is_weekend(now=None):
    now = now or datetime.now()
    return now.weekday() >= 5


print(is_weekend(datetime(2026, 10, 17)))
print(is_weekend(datetime(2026, 10, 19)))
```

```text
True
False
```

## What to do with a flaky test?

**Running it again is not a fix.** GitHub's "Re-run failed jobs" button
or plugins that retry a test a few times by themselves turn red into
green but hide the cause; a real bug passes the same way.

If it cannot be fixed right away, the test is put in **quarantine**: it
is set apart with a mark, it does not stop the main pipeline, but it
keeps running and stays visible:

```python
import pytest


@pytest.mark.flaky
def test_payment_timeout():
    assert True
```

```yaml
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q -m "not flaky"
  quarantine:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q -m flaky
```

- `-m "not flaky"` leaves out the marked tests; `-m flaky` runs only
  them.
- `continue-on-error: true`: even if the quarantine job fails, the run
  does not turn red.
- The mark is declared in `pyproject.toml` (`markers = ["flaky: ..."]`);
  otherwise pytest warns about an unknown mark.
- Quarantine is not a rubbish bin: every test in quarantine has an owner
  and a deadline. Otherwise the "temporary" list grows and the tests no
  longer check anything.

## Finding the cause of a failing pipeline

In a red run the order is:

1. **Which job, which step?** Open the red step on the run page.
2. **The first error line.** The end of the log is usually the result
   ("exit code 1"); the cause is further up. In pytest, the `FAILED`
   line and the `assert` line above it.
3. **Reproduce it locally.** The same Python version, the same package
   versions (easy if `requirements.txt` is pinned), the same command.
4. **If it cannot be reproduced, look at the differences:** operating
   system, time zone, package version, order.

You can also prepare the pipeline for debugging:

```yaml
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-report
          path: report.xml
```

- `timeout-minutes: 15` (seventh section): a hanging test does not keep the job waiting
  for hours. GitHub's default limit is 360 minutes.
- `--junitxml=report.xml` writes the results to a file a machine can
  read; how long each test took and which one failed are in it.
- With `if: failure()` the report is kept only when something failed
  (the artifact from the eighth section).
- For more detailed logs, define a variable or secret named
  `ACTIONS_STEP_DEBUG` with the value `true` in the repository, then
  start the run again choosing "debug logging".

## "It works on my machine"

| Difference | Your computer | The pipeline's machine |
|---|---|---|
| Operating system | Often Windows | `ubuntu-latest` (Linux) |
| Upper and lower case in file names | `Data.csv` = `data.csv` | Different files |
| Time zone | Your clock | UTC |
| Package version | Whatever came the day you installed | Whatever comes today (if not pinned) |
| Files left from before | There | None, the machine starts from scratch |

The last row is the most common: a folder you created by hand or a file
you downloaded earlier is making the tests pass on your computer; it is
not on the pipeline's clean machine.

## Next

The fifteenth section is the capstone project: we build the whole
pipeline of a Python project from start to finish.

## Summary

- A flaky test passes and fails without the code changing; as flaky
  tests add up, the chance of a green pipeline drops by multiplication
  and the trust in red is gone.
- Sources: order, time, randomness, set order, waiting, network.
- The order of a set of texts changes from process to process; do not
  rely on the order.
- A test that passes alone and fails together depends on order; with a
  fixture every test sets up its own data.
- The clock is passed in from outside; a fixed date in the test.
- Running again hides the cause; if it cannot be fixed, a quarantine with
  an owner and a deadline (`-m "not flaky"`, `continue-on-error`).
- When debugging: which step, the first error line, reproduce locally,
  the differences. `timeout-minutes`, `--junitxml` and keeping the report
  on failure.
