# The Matrix

Code has to work not only on your computer but on your users' computers
too: another operating system, another Python version. Writing a
separate job for each means copying the same steps five times. A
**matrix** makes one job definition produce a job for every combination
of the given values.

## One job, many copies

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

- Each key under `strategy.matrix` is a **dimension**; its list holds
  that dimension's values.
- GitHub runs a copy of the job for each combination: 2 operating
  systems × 2 Python versions = **4 jobs**.
- Inside a copy, the current value is read with `${{ matrix.os }}`,
  `${{ matrix.python-version }}`. `runs-on` can also come from the
  matrix.

Let us produce the combinations in Python. The Cartesian product (every
value with every value) with `itertools.product`:

```python
from itertools import product

matrix = {
    "os": ["ubuntu-latest", "windows-latest"],
    "python-version": ["3.12", "3.13"],
}

keys = list(matrix)
combos = [dict(zip(keys, values)) for values in product(*matrix.values())]
for combo in combos:
    print("test (" + ", ".join(combo.values()) + ")")
print(len(combos), "jobs")
```

```text
test (ubuntu-latest, 3.12)
test (ubuntu-latest, 3.13)
test (windows-latest, 3.12)
test (windows-latest, 3.13)
4 jobs
```

In GitHub's Actions tab the jobs appear with exactly these names:
`test (ubuntu-latest, 3.12)`. Which combination failed can be read from
the name.

The number of jobs is the **product** of the dimensions' lengths: 3
operating systems and 4 Python versions make 12 jobs; adding another
dimension multiplies the number. GitHub produces at most 256 jobs from a
matrix, but cost becomes a problem long before that limit.

## exclude and include

Not every combination may be needed. Two keys adjust the matrix:

<figure class="fig versus">
  <div><h4>exclude</h4><b>Removes</b> the combinations that match an entry in the list. The entry does not have to be a full combination: <code>os: windows-latest</code> alone removes every Windows job.</div>
  <div><h4>include</h4>If the entry matches existing combinations, it <b>adds new keys</b> to them; if it matches none, it is added as a <b>new combination</b>.</div>
  <figcaption>GitHub applies exclude first, then include.</figcaption>
</figure>

```yaml
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.13"]
        exclude:
          - os: windows-latest
            python-version: "3.12"
        include:
          - os: windows-latest
            slow: true
          - os: ubuntu-latest
            python-version: "3.14"
            experimental: true
```

Let us write these two rules in Python. A simplified model: an `include`
entry is added to a combination if its values for the matrix's
**original** keys are the same as that combination's:

```python
def apply(combos, keys, exclude, include):
    result = [combo for combo in combos
              if not any(all(combo[k] == v for k, v in rule.items())
                         for rule in exclude)]
    for extra in include:
        fits = [combo for combo in result
                if all(combo[k] == v for k, v in extra.items() if k in keys)]
        if fits:
            for combo in fits:
                combo.update(extra)
        else:
            result.append(dict(extra))
    return result


exclude = [{"os": "windows-latest", "python-version": "3.12"}]
include = [{"os": "windows-latest", "slow": True},
           {"os": "ubuntu-latest", "python-version": "3.14", "experimental": True}]
for combo in apply(combos, keys, exclude, include):
    print(combo)
```

```text
{'os': 'ubuntu-latest', 'python-version': '3.12'}
{'os': 'ubuntu-latest', 'python-version': '3.13'}
{'os': 'windows-latest', 'python-version': '3.13', 'slow': True}
{'os': 'ubuntu-latest', 'python-version': '3.14', 'experimental': True}
```

- `exclude` removed Windows + 3.12: 4 → 3.
- The first `include` entry (`os: windows-latest`) matched the remaining
  Windows job and added `slow: True` to it; it did not open a new job.
- The second entry's `python-version: "3.14"` is in no combination: since
  it could not match, it became a **new job**. 3 → 4.

A key added with `include` (`experimental`, `slow`) is read like the
matrix's other values: `${{ matrix.experimental }}`. It is empty in the
jobs it was not added to.

## A preview version: allowed to fail

Trying a Python version that is not out yet is a good early warning, but
the pipeline should not turn red when that job fails. The
`continue-on-error` from the fifth section is applied only to the trial
job, with a value from the matrix:

```yaml
  test:
    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.experimental == true }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest]
        python-version: ["3.12", "3.13"]
        include:
          - os: ubuntu-latest
            python-version: "3.14"
            experimental: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

`experimental` is `true` only in the 3.14 job; in the other jobs it is
empty, so the condition is false and the pipeline fails if they fail.

## fail-fast and max-parallel

<figure class="fig anat">
  <div class="anat-row"><span><code>fail-fast</code></span><span>The default is <code>true</code>: when a job in the matrix fails, the other running and queued jobs are cancelled. With <code>false</code>, all of them run to the end.</span></div>
  <div class="anat-row"><span><code>max-parallel</code></span><span>At most how many jobs run at the same time. If not written, GitHub starts as many jobs as it can.</span></div>
</figure>

`fail-fast: true` saves machine minutes; but the jobs stop before you
learn whether a mistake happens only on Windows or everywhere. If you
want to see which combinations have the mistake, use
`fail-fast: false`.

## Time and cost

A matrix separates two different times: **wall clock** (the time from
the start of the pipeline to the end) and **machine minutes** (the total
time all machines spend). Let each test job take 6 minutes:

```python
import math

jobs = 6
minutes = 6
print("machine minutes:", jobs * minutes)
for limit in (None, 2):
    parallel = jobs if limit is None else limit
    rounds = math.ceil(jobs / parallel)
    print("max-parallel", limit, "-> wall clock", rounds * minutes, "min")
```

```text
machine minutes: 36
max-parallel None -> wall clock 6 min
max-parallel 2 -> wall clock 18 min
```

A matrix keeps the wall clock short (the jobs run at the same time), but
machine minutes grow with the number of jobs. In public repositories
GitHub's standard machines are free; private repositories have a monthly
allowance of minutes, and Windows and macOS minutes count as more
expensive than Linux. That is why a matrix is usually set up like this:
all Python versions on Linux, the other operating systems with only one
version.

## Which values?

- **Python versions:** at least the oldest and newest version you say
  you support. If a version in between breaks, add it too.
- **Operating systems:** the ones your users really use. Differences
  like file paths, line endings and case sensitivity usually show up on
  Windows.
- **Write versions in quotes:** `["3.12", "3.13"]`. The trap from the
  third section applies to the matrix too: unquoted `3.10` becomes
  `3.1`.

## Summary

- `strategy.matrix`: each key is a dimension; the number of jobs is the
  product of the dimensions. A value is read with `${{ matrix.<name> }}`.
- Job names show the combination: `test (ubuntu-latest, 3.12)`.
- `exclude` removes matching combinations; `include` adds keys to a
  matching combination and makes a new job from one that does not match.
  Exclude first, then include.
- `fail-fast` is `true` by default; `false` to see where the mistake is.
- `continue-on-error: ${{ matrix.experimental == true }}` lets only the
  trial job fail.
- The wall clock gets shorter; machine minutes grow with the number of
  jobs.
