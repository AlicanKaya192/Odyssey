# Jobs and Dependencies

The workflows so far mostly had a single job. A real pipeline has
several: code checks (lint), tests, building the package, deployment. In
this section we see how jobs run **at the same time**, how they are put
**in order** with `needs`, what happens to the others when a job fails,
and how a job is skipped with a condition (`if`).

## Jobs run at the same time

If a workflow has several jobs, GitHub starts all of them **at the same
time**. Each job runs on its own clean machine:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest
```

`lint` and `test` do not wait for each other. Two things follow:

- **Time is saved:** a two-minute lint and a six-minute test finish in
  six minutes in total, not eight.
- **Jobs do not share files:** since each job is on a separate machine,
  each one gets the code itself (`checkout`). A file one job produces
  does not exist in the other; we will see how to move files between
  jobs in the eighth section.

## needs: putting them in order

Some jobs must wait for another to finish: the package should not be
built before the tests pass, and there is no deployment without a
package. `needs` says this:

```yaml
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: echo "build"
```

`build` starts when `lint` and `test` have **both finished
successfully**. For a single job you can also write `needs: test`.

The jobs and the `needs` arrows between them form a **directed graph**
(the DAG from the Algorithm Techniques module). GitHub works out from
this graph when each job starts. Let us do the same calculation in
Python: a **wave** is the set of jobs whose awaited jobs have all
finished; the jobs in a wave can run at the same time.

```python
needs = {
    "lint": [],
    "test": [],
    "docs": [],
    "build": ["lint", "test"],
    "deploy": ["build"],
}


def waves(needs):
    done = []
    result = []
    while len(done) < len(needs):
        wave = [job for job in needs
                if job not in done and all(n in done for n in needs[job])]
        if not wave:
            raise ValueError("circular needs: " + ", ".join(
                job for job in needs if job not in done))
        result.append(wave)
        done += wave
    return result


for number, wave in enumerate(waves(needs), start=1):
    print(number, wave)
```

```text
1 ['lint', 'test', 'docs']
2 ['build']
3 ['deploy']
```

Three waves: first `lint`, `test` and `docs` together, then `build`,
last `deploy`.

## Total time and the critical path

A job's finishing time is its own duration plus the finishing time of
the **latest** of the jobs it waits for. Let the durations be minutes:

```python
minutes = {"lint": 1, "test": 6, "docs": 2, "build": 3, "deploy": 2}

finish = {}
for wave in waves(needs):
    for job in wave:
        start = max([finish[n] for n in needs[job]], default=0)
        finish[job] = start + minutes[job]

print("finish:", finish)
print("pipeline:", max(finish.values()), "min")
print("one by one:", sum(minutes.values()), "min")
```

```text
finish: {'lint': 1, 'test': 6, 'docs': 2, 'build': 9, 'deploy': 11}
pipeline: 11 min
one by one: 14 min
```

The pipeline finishes in 11 minutes; if the jobs ran one by one it would
take 14. The chain that sets the 11 minutes is `test → build → deploy`:
this is called the **critical path**. Making `lint` twice as fast would
not shorten the pipeline by a second; whoever wants a faster pipeline
looks at the job on the critical path (here `test`).

## A cycle

If job `a` waits for `b` and `b` waits for `a`, neither can start. GitHub
does not run such a file. Our `waves` function also stops when it cannot
find a job that can start:

```python
try:
    waves({"build": ["test"], "test": ["build"]})
except ValueError as error:
    print(error)
```

```text
circular needs: build, test
```

Writing `needs` for a job that does not exist (`needs: tests` when the
job is called `test`) also makes the file invalid. Odyssey's check
catches both.

## When a job fails

The default rule: a job runs if **all** the jobs it waits for
succeeded. If one fails, the jobs that depend on it are **skipped**, and
so are the ones that depend on those. The job's `if` condition can
change this rule. There are three **status functions** used in
conditions:

<figure class="fig anat">
  <div class="anat-row"><span><code>success()</code></span><span>All the previous jobs succeeded. This is what applies if no <code>if</code> is written.</span></div>
  <div class="anat-row"><span><code>failure()</code></span><span>One of the previous jobs (including ones further back in the chain) failed. For failure notifications.</span></div>
  <div class="anat-row"><span><code>always()</code></span><span>Run no matter what. For cleaning up or reporting.</span></div>
</figure>

Let us write these rules in Python and see what happens to each job when
`test` fails. `notify` should run only when something fails, `report`
always:

```python
pipeline = {
    "lint": [],
    "test": [],
    "build": ["lint", "test"],
    "deploy": ["build"],
    "notify": ["deploy"],
    "report": ["deploy"],
}
conditions = {"notify": "failure()", "report": "always()"}


def ancestors(needs, job):
    found = set()
    for parent in needs[job]:
        found |= {parent} | ancestors(needs, parent)
    return found


def statuses(needs, failed, conditions):
    status = {}
    for wave in waves(needs):
        for job in wave:
            condition = conditions.get(job, "success()")
            if condition == "always()":
                runs = True
            elif condition == "failure()":
                runs = any(status[a] == "failure" for a in ancestors(needs, job))
            else:
                runs = all(status[n] == "success" for n in needs[job])
            if not runs:
                status[job] = "skipped"
            elif job in failed:
                status[job] = "failure"
            else:
                status[job] = "success"
    return status


for job, state in statuses(pipeline, {"test"}, conditions).items():
    print(f"{job:<7} {state}")
```

```text
lint    success
test    failure
build   skipped
deploy  skipped
notify  success
report  success
```

- `test` failed → `build` was skipped → `deploy` was skipped too.
- `notify`'s `if: failure()` condition sees `test`, which failed further
  back at the start of the chain, and runs; if it only looked at
  `deploy`, the job it waits for directly (`deploy` was skipped, it did
  not fail), it would never run.
- `report` runs because it is `always()`.

## Conditions with if

`if` is used not only for the status but also to decide by event and
branch. The condition reads GitHub's **context** values:

<figure class="fig anat">
  <div class="anat-row"><span><code>github.event_name</code></span><span>The event that started the workflow: <code>push</code>, <code>pull_request</code>...</span></div>
  <div class="anat-row"><span><code>github.ref</code></span><span>The branch or tag: <code>refs/heads/main</code>, <code>refs/tags/v1.2.0</code>.</span></div>
  <div class="anat-row"><span><code>github.actor</code></span><span>The user who started the run.</span></div>
  <div class="anat-row"><span><code>needs.&lt;job&gt;.result</code></span><span>The result of an awaited job: <code>success</code>, <code>failure</code>, <code>skipped</code>.</span></div>
</figure>

The most common example: deploy only on a push to `main`, not on PRs.

```yaml
  deploy:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

How a condition is written:

- Text is written in **single quotes**: `'refs/heads/main'`.
- `&&` means "and", `||` "or", `!` "not".
- In an `if` value you do not need `${{ }}`; GitHub already reads it as
  an expression.
- If no status function other than `success()` is used, `success() &&`
  is added in front of the condition automatically: a job with
  `if: github.ref == ...` still does not run if the jobs it waits for
  failed.

## Passing a value from job to job

Jobs do not share files, but they can pass a small **value**. The value
is written in a step as `name=value` to the `$GITHUB_OUTPUT` file,
exposed in the job's `outputs` section, and read in the other job with
`needs.<job>.outputs.<name>`:

```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      number: ${{ steps.read.outputs.number }}
    steps:
      - uses: actions/checkout@v4
      - id: read
        run: echo "number=$(cat VERSION)" >> "$GITHUB_OUTPUT"
  build:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building ${{ needs.version.outputs.number }}"
```

The step's `id` (`read`) gives its output a name. This suits small texts
like a version number or a list of changed folders; not files.

## Going on despite errors

A failing job fails the pipeline. Sometimes a job runs "for information":
for example trying a Python version that is not out yet. If that job has
`continue-on-error: true`, the run counts as successful even if it fails.
Use it rarely: if it is written everywhere, the pipeline stops nothing.

## All together

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python -m pytest
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip wheel . -w dist
  deploy:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
  notify:
    needs: deploy
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: echo "The pipeline failed on ${{ github.ref }}"
```

## Summary

- By default jobs run at the same time on separate machines; they do not
  share files.
- `needs` sets an order; the jobs form a directed graph. A cycle and
  `needs` for a missing job are invalid.
- The pipeline's time is set by the **critical path**; to speed it up,
  look at the job there.
- When a job fails, the jobs depending on it are skipped. `failure()`
  also sees a job that failed further back in the chain; `always()`
  always runs.
- `if` reads the context: `github.event_name`, `github.ref`. Text in
  single quotes.
- Small values are passed via `$GITHUB_OUTPUT` → `outputs` →
  `needs.<job>.outputs`.
