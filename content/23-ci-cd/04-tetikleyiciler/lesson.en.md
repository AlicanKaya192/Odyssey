# Triggers

Every workflow we have written so far started with `on: push`: it ran on
every push to the repository. In a real project this is often too much or
too little. Running a twenty-minute test pipeline for a commit that fixes
the documentation is wasted time; a pull request, on the other hand,
should be tested **before** it is merged. In this section we look at the
events the `on` key can take and the **filters** that narrow them down.

## What is an event?

GitHub gives a name to everything that happens in a repository: a push is
`push`, a pull request is `pull_request`, a time arriving is `schedule`,
someone pressing a button is `workflow_dispatch`. The workflow's `on`
section says "run me when one of these events happens". `on` can be
written in three forms:

```yaml
on: push
```

```yaml
on: [push, pull_request]
```

```yaml
on:
  push:
    branches: [main]
  pull_request:
```

In the third form you can write settings under each event. An event
without settings (`pull_request:`) is left empty.

## push and pull_request

These two are the most used events, and their difference matters:

<figure class="fig versus">
  <div><h4>push</h4>When commits are pushed to a branch. The workflow runs on <b>that commit</b>.</div>
  <div><h4>pull_request</h4>When a pull request is opened, gets new commits or is reopened. The workflow runs on the PR <b>merged</b> with the target branch.</div>
  <figcaption>pull_request answers "what happens once this is merged" before the merge.</figcaption>
</figure>

Let us open up the second point. The tests on your branch may pass; but
if someone added a change to `main` while you were working, the tests may
fail once the two are merged. Because the `pull_request` event runs on a
merge commit GitHub prepares in advance, it catches this before anyone
presses the merge button.

A common setup uses both:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

- `push` → every commit that reaches `main` is tested (including after a
  merge).
- `pull_request` → every PR opened against `main` is tested before it is
  merged.

Careful: the `branches` under `pull_request` is the PR's **target**
branch (the branch it will be merged into), not the branch you opened the
PR from.

There is also a **double run** trap. With an unfiltered
`on: [push, pull_request]`, pushing a commit to the branch of an open PR
creates two events: a push to the branch (`push`) and a new commit on the
PR (`pull_request`). The same tests run twice. Limiting `push` to `main`
prevents this.

## The branch filter

`branches` says which branches to run on, `branches-ignore` which
branches not to run on. Both cannot be written for the same event. The
values are **patterns**:

<figure class="fig anat">
  <div class="anat-row"><span><code>main</code></span><span>Only the <code>main</code> branch.</span></div>
  <div class="anat-row"><span><code>release/*</code></span><span>Branches like <code>release/1.0</code> that start with <code>release/</code> and contain no other <code>/</code>.</span></div>
  <div class="anat-row"><span><code>release/**</code></span><span>Every branch that starts with <code>release/</code>, <code>release/2026/oct</code> included.</span></div>
</figure>

The difference between the two signs: `*` matches anything except a
slash (`/`), `**` matches anything including a slash. Let us imitate this
rule with a small Python function. It turns the pattern into a regular
expression: `**` → `.*`, `*` → `[^/]*` ("anything that is not a slash"):

```python
import re


def matches(pattern, path):
    regex = ""
    i = 0
    while i < len(pattern):
        if pattern[i:i + 2] == "**":
            regex += ".*"
            i += 2
        elif pattern[i] == "*":
            regex += "[^/]*"
            i += 1
        else:
            regex += re.escape(pattern[i])
            i += 1
    return re.fullmatch(regex, path) is not None


for pattern, path in [("release/*", "release/1.0"),
                      ("release/*", "release/2026/oct"),
                      ("release/**", "release/2026/oct"),
                      ("*.md", "README.md"),
                      ("*.md", "docs/guide.md"),
                      ("**.md", "docs/guide.md"),
                      ("docs/**", "docs/img/logo.png")]:
    print(f"{pattern:<11} {path:<18} {matches(pattern, path)}")
```

```text
release/*   release/1.0        True
release/*   release/2026/oct   False
release/**  release/2026/oct   True
*.md        README.md          True
*.md        docs/guide.md      False
**.md       docs/guide.md      True
docs/**     docs/img/logo.png  True
```

The most surprising line is `*.md`: it only matches `.md` files at the
**root** of the repository, not `docs/guide.md`. For `.md` files in every
folder you write `**.md`.

This function is a simplified model. GitHub's patterns have a few more
signs (`?`, `[]`, a leading `!` for "exclude"); but most daily work is
done with `*` and `**`.

## The path filter

`paths` says "run only if one of these files changed"; `paths-ignore`
says "do not run if **all** the changed files are among these". This is
how you skip the test pipeline for documentation:

```yaml
on:
  push:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "**.md"
```

If the branch and path filters are written together, **both conditions**
must hold. Let us write GitHub's decision in Python. We use the `matches`
function from above:

```python
def would_run(branch, changed, branches, ignored):
    if not any(matches(pattern, branch) for pattern in branches):
        return False
    for path in changed:
        if not any(matches(pattern, path) for pattern in ignored):
            return True
    return False


ignored = ["docs/**", "**.md"]
print(would_run("main", ["docs/setup.md"], ["main"], ignored))
print(would_run("main", ["README.md", "app/core.py"], ["main"], ignored))
print(would_run("feature/login", ["app/core.py"], ["main"], ignored))
```

```text
False
True
False
```

1. Only documentation changed → it does not run.
2. A document and a code file changed → it runs: not all the changed
   files are ignored ones.
3. Code changed but the branch is not `main` → it does not run.

## Tags

When releasing, a **tag** like `v1.2.0` is put on a commit (we saw this
in the Git path). Pushing the tag is also a `push` event, and it is
caught with the `tags` filter:

```yaml
on:
  push:
    tags: ["v*"]
```

A trap: if an event has only `tags`, pushes to branches **no longer
start** that workflow; if it has only `branches`, tag pushes do not start
it. If you want both, write both. We will see workflows that make
releases in the eighth section.

## Scheduled runs

`schedule` ties the workflow to a calendar. The time is written as a
**cron** expression: five fields separated by spaces.

<figure class="fig anat">
  <div class="anat-row"><span>1. minute</span><span>0–59</span></div>
  <div class="anat-row"><span>2. hour</span><span>0–23</span></div>
  <div class="anat-row"><span>3. day of the month</span><span>1–31</span></div>
  <div class="anat-row"><span>4. month</span><span>1–12</span></div>
  <div class="anat-row"><span>5. day of the week</span><span>0–6, <b>0 = Sunday</b>, 1 = Monday</span></div>
</figure>

`*` means "every value". `30 2 * * 1` → every Monday at 02:30. The time
is always **UTC**; Turkey is 3 hours ahead of UTC. Let us compute when a
cron expression runs. To keep it short we write a matcher that only
knows `*`, numbers and comma lists (`1,3,5`):

```python
from datetime import datetime, timedelta


def field_ok(field, value):
    return field == "*" or str(value) in field.split(",")


def next_runs(cron, start, count):
    minute, hour, day, month, weekday = cron.split()
    runs = []
    moment = start
    while len(runs) < count:
        moment += timedelta(minutes=1)
        cron_weekday = (moment.weekday() + 1) % 7
        if (field_ok(minute, moment.minute) and field_ok(hour, moment.hour)
                and field_ok(day, moment.day) and field_ok(month, moment.month)
                and field_ok(weekday, cron_weekday)):
            runs.append(moment)
    return runs


start = datetime(2026, 10, 14, 12, 0)
for run in next_runs("30 2 * * 1", start, 3):
    turkey = run + timedelta(hours=3)
    print("UTC", run.strftime("%Y-%m-%d %H:%M"), "| TR", turkey.strftime("%H:%M"))
```

```text
UTC 2026-10-19 02:30 | TR 05:30
UTC 2026-10-26 02:30 | TR 05:30
UTC 2026-11-02 02:30 | TR 05:30
```

Two details:

- Python's `weekday()` counts Monday as 0, cron counts Sunday as 0.
  `(weekday() + 1) % 7` fixes this shift.
- 02:30 UTC is 05:30 in Turkey. If you want "every morning at 06:00
  Turkey time", you write `0 3 * * *` in the cron.

What to know about GitHub's scheduled runs:

- The schedule is read only from the workflow file on the **default
  branch** (usually `main`).
- It can run at most once every 5 minutes.
- When GitHub is busy the run can be delayed; the busiest moment is the
  top of the hour. Picking a minute like `17` instead of `0` reduces the
  delay.
- In a public repository, scheduled workflows are disabled automatically
  after 60 days without any activity.

What is it for? All the tests at night (quick ones on every push, slow
ones at night), trying the newest versions of dependencies, a weekly
report.

## Starting by hand

The `workflow_dispatch` event adds a **Run workflow** button to the
workflow in GitHub's Actions tab. It is used to try a scheduled workflow
without waiting, or to start a deployment by hand. You can also define
**inputs** asked when the button is pressed:

```yaml
on:
  workflow_dispatch:
    inputs:
      level:
        description: "How many tests to run"
        type: choice
        options: [quick, full]
        default: quick
```

Inside the workflow the input is read with `${{ inputs.level }}`. The
button also appears only if the file on the default branch has
`workflow_dispatch`.

## Skipping a run

If `[skip ci]` is written in a commit message, the `push` and
`pull_request` runs that push would start are skipped. It is useful for a
commit that only fixes a typo; but if it becomes a habit, untested code
gets into `main`. For documentation, `paths-ignore` is a safer way.

## All together

```yaml
name: CI

on:
  push:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "**.md"
  pull_request:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "**.md"
  schedule:
    - cron: "17 3 * * *"
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

This workflow runs on code changes that reach `main`, on PRs opened
against `main`, every night at 03:17 UTC (06:17 in Turkey) and by hand
when asked; it does not run if only documentation changes.

## Summary

- `on` lists events: `push`, `pull_request`, `schedule`,
  `workflow_dispatch`...
- `pull_request` tests the merged result; the `branches` under it is the
  target branch. Limiting `push` to `main` prevents double runs.
- In patterns `*` does not match a slash, `**` does. `*.md` is only the
  files at the root.
- `paths-ignore`: if all the changed files are ignored ones, it does not
  run. Branch and path filters together: both conditions must hold.
- `tags: ["v*"]` catches tag pushes; with only `tags`, branch pushes do
  not start it.
- cron has five fields, the time is **UTC**, day of the week 0 = Sunday.
- `workflow_dispatch` is a button to start by hand, with inputs.
