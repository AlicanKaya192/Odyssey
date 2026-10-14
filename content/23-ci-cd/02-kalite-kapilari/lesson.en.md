# Code Quality Gates

Tests tell you whether the code works **correctly**. But code that works
correctly can still be unreadable, inconsistent or dangerous: unused
imports, forgotten `print` lines, a different writing style in every
file, branches that no test ever touches. The **quality gates** in the
pipeline catch these. In this section we look at which gates there are, in
which order they go into the pipeline, and how a gate decides between
"pass" and "fail".

## What a gate is

A **gate** is a stage that checks a rule and stops the pipeline if the
rule does not hold. The test stage is a gate too: if a test fails, the
pipeline stops. Quality gates work the same way; only what they check is
different.

Every gate has two parts:

- **The measurement:** a tool looks at the code and counts or finds
  something (long lines, unused names, untested lines).
- **The threshold:** below or above which value the gate closes ("no lint
  errors at all", "coverage at least 80%").

A gate reports its decision, as we saw with tests, through the **exit
code**: `0` if the rule holds, a number other than `0` if it does not.

## Common gates

<figure class="fig anat">
  <div class="anat-row"><span>Syntax</span><span>Can the code be read as Python? The fastest gate.</span></div>
  <div class="anat-row"><span>Format</span><span>Are indentation, spaces, quotes and line length the same everywhere? (formatter)</span></div>
  <div class="anat-row"><span>Lint</span><span>Mistakes that can be found without running the code: an unused import, an undefined name, a shadowed variable. (static analysis)</span></div>
  <div class="anat-row"><span>Type check</span><span>Are the type hints consistent with each other?</span></div>
  <div class="anat-row"><span>Tests</span><span>Do all the tests pass?</span></div>
  <div class="anat-row"><span>Coverage</span><span>How much of the code did the tests run?</span></div>
</figure>

**Static analysis** means examining code by reading it, without running
it. It is fast and sees every path of the program, but it cannot know what
the program will do while it runs. Tests are the opposite: they really run
the code but only see the paths they try. The two complete each other.

## The fastest gate: syntax

Every Python installation has a ready gate: `py_compile` compiles a file
without running it and ends with exit code `1` if there is a syntax
error. We tried a file with an unclosed bracket and a healthy file:

```python
import subprocess
import sys
from pathlib import Path

Path("good.py").write_text("print('hello')\n")
Path("broken.py").write_text("print('hello'\n")

for name in ["good.py", "broken.py"]:
    command = [sys.executable, "-m", "py_compile", name]
    result = subprocess.run(command, capture_output=True, text=True)
    print(name, "-> exit code", result.returncode)
```

```text
good.py -> exit code 0
broken.py -> exit code 1
```

This gate takes less than a second, so it goes at the very start of the
pipeline: if the code cannot be read, there is no point installing the
tests.

## Format and lint: the real-world tools

One of the most common tools in Python projects today is **ruff**: it both
lints and formats code. There are older tools for the same jobs too
(flake8 and pylint for lint, black for format). In a pipeline it runs like
this:

```text
pip install ruff
ruff check .
ruff format --check .
```

- `ruff check .` checks the lint rules in every file in the folder. If a
  rule is broken, it prints the file, the line and the code of the rule,
  and the exit code is not `0`.
- `ruff format .` **fixes** the files. In a pipeline it runs with
  `--check`: it does not touch the files, it only says "this file is not
  formatted" and closes the gate. We do not want the pipeline to change
  the code; the developer makes the fix on their own computer.

These tools are not installed in Odyssey; you will use the commands in
your own project. In this section's exercises you build the same idea on
a small scale with your own code: a gate that finds long lines and
forgotten `print`s.

For **type checking** the most common tool is **mypy**: `mypy .` looks at
the type hints and finds, without running the code, that a `str` is given
where an `int` is expected.

## Coverage: how much of the code did the tests touch

**Coverage** measures which lines of the code ran at least once while the
tests were running. The common tool is **coverage.py**, used with pytest
through the `pytest-cov` plugin:

```text
python -m pytest --cov=cart --cov-fail-under=80
```

`--cov-fail-under=80` fails the command if coverage is below 80 percent:
that is a threshold.

What does a coverage tool do inside? We can see the same thing on a small
scale with Python's own `trace` module. `cart.py` from the previous
section looked like this (think of it with line numbers):

```python
def cart_total(prices, discount=0):
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
```

Let us run only the two tests without a discount and count which lines
ran:

```python
import trace

from cart import cart_total


def test_total_without_discount():
    assert cart_total([10, 20, 30]) == 60


def test_empty_cart():
    assert cart_total([]) == 0


tracer = trace.Trace(count=1, trace=0)
tracer.runfunc(test_total_without_discount)
tracer.runfunc(test_empty_cart)

body = range(2, 8)
ran = sorted(line for (file, line) in tracer.results().counts if file.endswith("cart.py"))
missed = [line for line in body if line not in ran]
print("ran:", ran)
print("missed:", missed)
print("coverage:", round(100 * len(ran) / len(body)), "%")
```

```text
ran: [2, 4, 5, 7]
missed: [3, 6]
coverage: 67 %
```

Both tests passed, but line 3 (the error) and line 6 (the discount)
**never** ran. The `/ 10` mistake from the previous section was exactly on
line 6: with these two tests the pipeline stays green and the mistake
reaches the users. Coverage makes this visible.

After adding the discount test and two error tests, the same measurement:

```text
ran: [2, 3, 4, 5, 6, 7]
missed: []
coverage: 100 %
```

## What coverage does not tell you

- **100% coverage does not mean the code is correct.** A line ran, but
  there may be no `assert` that checks its result. A test without an
  `assert` raises coverage too.
- It is easy to write meaningless tests to raise coverage. That is why
  the threshold is kept reasonable (70–90% is common), and the real
  question is: **are the important branches tested?**
- A good habit: do not let coverage **go down**. If new code is added
  without tests, the gate closes.

## The order of the gates

The fail fast rule applies to gates too. Cheap gates go first:

<figure class="fig">
  <div class="flow">
    <span class="node">Syntax</span>
    <span class="arrow">→</span>
    <span class="node">Format</span>
    <span class="arrow">→</span>
    <span class="node">Lint</span>
    <span class="arrow">→</span>
    <span class="node acc">Tests</span>
    <span class="arrow">→</span>
    <span class="node">Coverage</span>
  </div>
  <figcaption>Gates that take seconds go first, tests that take minutes go last.</figcaption>
</figure>

In a workflow this means the order of the steps:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install ruff
      - run: ruff check .
      - run: ruff format --check .
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

If format or lint fails, the tests are not even installed; the feedback
arrives within seconds.

## Run the gates locally too

A format gate that fails in the pipeline means waiting for the whole
pipeline again for a one-minute fix. That is why teams run the same
commands on their own computers before pushing. There are tools that do
this automatically (**pre-commit** hooks that run before a commit); the
idea is the same: catch what the pipeline would catch before it gets
there.

## Summary

- A gate = a measurement + a threshold; it reports its decision through
  the exit code.
- Static analysis reads code without running it (format, lint, types);
  tests run the code. The two complete each other.
- In a pipeline the formatter runs with `--check` and does not change the
  files.
- Coverage shows the untested lines; 100% coverage does not mean
  correctness.
- Cheap gates first: syntax, format, lint, then the tests.
