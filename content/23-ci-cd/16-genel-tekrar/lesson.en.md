# Overall Review

You have reached the end of the CI/CD and DevOps module. We started with
the "it worked on my machine" problem; we put tests and quality gates
into the pipeline and read the workflow file piece by piece. Then we
managed the pipeline: when it runs, which job waits for which, the matrix
and caching. After that we moved to the product: the package, secrets,
versions and deployment. At the end we saw working as a team, flaky tests
and the whole pipeline of a project. This section walks the path once
more.

<figure class="fig">
  <div class="flow">
    <span class="node">Tests and gates</span>
    <span class="arrow">→</span>
    <span class="node">Manage the pipeline</span>
    <span class="arrow">→</span>
    <span class="node">Product and security</span>
    <span class="arrow">→</span>
    <span class="node">Production and team</span>
    <span class="arrow">→</span>
    <span class="node acc">Full pipeline</span>
  </div>
  <figcaption>The module's path: test, organise, package and protect, go live, put it together.</figcaption>
</figure>

## 1. The basics (Sections 0–3)

- **CI:** merge often; on every merge the code is set up and tested on a
  clean machine. **Continuous delivery:** every change that passes is
  ready to release; a person starts the release. **Continuous
  deployment:** the release happens by itself too (0).
- **pytest** finds `test_` files and functions; the pipeline decides from
  the exit code: `0` passed, `1` failed, `5` no tests (1).
- **A gate** = a measurement + a threshold. Cheap gates first: syntax,
  format, lint, then tests; coverage shows untested lines but is not
  proof of correctness (2).
- **The workflow file** is a tree of dictionaries and lists: `on`,
  `jobs` → `runs-on`, `steps`; a step is either `uses` or `run`. Versions
  in quotes (`"3.10"`) (3).

## 2. Managing the pipeline (Sections 4–7)

- **Triggers:** `pull_request` tests the merged form; `branches` is the
  target branch. `*` does not match a slash, `**` does. cron is UTC (4).
- **Jobs** run at the same time on separate machines; `needs` sets an
  order. The **critical path** sets the duration. `failure()`,
  `always()`; `outputs` to pass values (5).
- **Matrix:** the number of jobs is the product of the dimensions;
  `exclude` first, `include` after; `fail-fast: false` to see where it
  fails (6).
- **Speed:** a cache key from content (`hashFiles`), `cache: pip`;
  `concurrency` cancels the old run; `timeout-minutes` (7).

## 3. Product and security (Sections 8–10)

- **An artifact** is for the product, a cache for speed. **Build once:**
  the tested and the released file are the same (8).
- **A secret** stays in the vault and goes through `env:` only to the step
  that asks; it is empty in a fork's PR. `permissions:` least privilege.
  Text from outside is not written straight into `run:` (9).
- **Versions:** `MAJOR.MINOR.PATCH`, compared as numbers; commit prefixes
  say the bump; the tag must match `pyproject.toml`, a released tag is
  not moved (10).

## 4. Going live and the team (Sections 11–14)

- **Deployment:** staging first, then production; environments carry
  approval and environment secrets. Rolling, blue-green, canary; a health
  check and rollback with `if: failure()`; `cancel-in-progress: false`
  for deployments (11).
- **Containers:** build the image, test inside it, send the same image;
  deploy with a tag that does not change (SHA), `packages: write` for
  `ghcr.io`, the layer cache `type=gha` (12).
- **The team:** `main` is protected by rules; a required check's name is
  the job's name; if the name changes or the workflow never starts, the
  PR waits; one gate job `ci-ok`; `merge_group` for the queue (13).
- **A flaky test** destroys trust: twenty of them make the pipeline red
  for no reason in one run out of three. Order, time, set order; not
  re-running but fixing, or a quarantine with an owner (14).

## 5. The full pipeline (Section 15)

- The contract first, then the YAML: triggers, lint → matrix tests →
  package → `ci-ok` → release on a tag; read permission at the top, write
  only in the release; a critical path of 7 minutes (15).

## All together: reviewing a pipeline

Using the module's rules, let's write a small reviewer that reads a
workflow file and lists its problems. The file below has four mistakes
we saw in this module:

```python
import re

import yaml

TEXT = """
name: CI
on: [push, pull_request]
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - run: echo "${{ github.event.pull_request.title }}"
      - run: python -m pytest
"""


def review(text):
    data = yaml.safe_load(text)
    problems = []
    if data.get("permissions") in (None, "write-all"):
        problems.append("permissions: read by default")
    for name, job in data["jobs"].items():
        if "timeout-minutes" not in job:
            problems.append(f"{name}: no timeout-minutes")
        for step in job["steps"]:
            uses = step.get("uses", "")
            if uses and "@" not in uses:
                problems.append(f"{name}: {uses} has no version")
            if re.search(r"\$\{\{\s*github\.event\.", step.get("run", "")):
                problems.append(f"{name}: outside text in run")
    return problems


for problem in review(TEXT):
    print(problem)
```

```text
permissions: read by default
test: no timeout-minutes
test: actions/checkout has no version
test: outside text in run
```

Every line rests on a section: permissions (9), the time limit (7), an
action without a version (3 and 9), code injection (9). Real projects
have ready-made tools that do this; but knowing what they look at is the
only way to understand their warnings.

## After this

In this module we checked workflows without running them; the tests and
scripts really ran. When you set up the first pipeline in your own
repository, the only thing that changes is that the file really runs on
GitHub's machine. The rules stay the same: **start small, put the fast
gate first, be able to say why each piece is there.**

The second module of this path is **MLOps and ML System Design**: the
same pipeline is used to train, measure and serve a model.
