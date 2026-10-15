# Branch Strategy and PR Checks

So far we thought of the pipeline as if one person used it. In a team,
many people send code to the same repository every day. The `main`
branch must stay **working at all times**, and nobody should be able to
put code there whose tests do not pass. In this section we see how to
organise branches, how to protect `main` with GitHub's rules and which
traps the checks that run in a PR fall into.

## Branch strategies

A branch strategy is the team's agreed answer to the question "who works
on which branch, and how does code get into `main`". Three common ones:

| Strategy | How | When it fits |
|---|---|---|
| Trunk-based | Very short-lived branches (a day or two), merging into `main` often | Teams with strong tests that deploy often |
| GitHub flow | A branch per piece of work, PR, review, merge into `main`; `main` is deployable at any time | Most projects; the layout this path assumes |
| GitFlow | `main` + `develop` + feature, release and hotfix branches | Projects that release rarely and on a plan |

The common idea: the longer a branch lives, the further it drifts from
`main` and the harder it is to merge. CI's promise of "merge often"
(section zero) goes through keeping branches short.

## Protecting `main`

On GitHub, rules for `main` are written on the repository's
**Settings › Rules** page (rulesets), or under the older name
**Branches › Branch protection**:

- **Require a PR**: no direct pushes to `main`; every change goes
  through a PR.
- **Require approval**: it cannot be merged until at least one person
  approves the PR.
- **Required status checks**: the merge button stays closed until the
  checks on the list pass.
- **Require the branch to be up to date**: the PR cannot be merged
  without being tested again with the latest `main`.
- **Block force pushes and deletion**: `main`'s history cannot be
  rewritten.

The pipeline's work starts at the third of these rules: the pipeline
produces the checks that let a PR through or stop it.

## A required check's name is the job's name

The required check list holds **the job's name**, not the workflow's
name: `lint`, `test`. In a matrix job every copy is a separate check and
GitHub shows them with names like `test (3.12)`, `test (3.13)`. Let's see
the merge decision with a small model:

```python
def matrix_names(job, versions):
    return [f"{job} ({version})" for version in versions]


def merge_state(required, reported):
    for name in required:
        if reported.get(name) == "failure":
            return f"blocked: {name} failed"
    for name in required:
        if reported.get(name) != "success":
            return f"waiting: {name}"
    return "ready"


required = ["lint"] + matrix_names("test", ["3.12", "3.13"])
print(required)
runs = {"lint": "success", "test (3.12)": "success",
        "test (3.13)": "success"}
print(merge_state(required, runs))
runs["test (3.13)"] = "failure"
print(merge_state(required, runs))
renamed = {"lint": "success", "tests (3.12)": "success",
           "tests (3.13)": "success"}
print(merge_state(required, renamed))
```

```text
['lint', 'test (3.12)', 'test (3.13)']
ready
blocked: test (3.13) failed
waiting: test (3.12)
```

The last line is the most common trap: someone renamed the `test` job to
`tests` in the workflow. All checks pass, but the required list still
says `test (3.12)` and no result comes with that name. The PR **waits
forever**; GitHub shows it as "Expected — Waiting for status to be
reported". When a job's name changes, the rule is updated too.

## A workflow that never runs: the gate job

The second way into the same trap is the path filter from the fourth
section. In a PR that only changes `README.md`, a workflow filtered with
`paths: ["src/**"]` **never starts**. A workflow that does not start
reports no result either; the required check waits again. A commit with
`[skip ci]` ends up in the same place.

The difference is this: if the workflow starts and a job is **skipped**
by an `if:`, GitHub counts that job as successful for the required check.
The common solution is to write one **gate job** that depends on all the
jobs and put only that one on the required list:

```yaml
  ci-ok:
    if: always()
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
        if: >-
          contains(needs.*.result, 'failure')
          || contains(needs.*.result, 'cancelled')
      - run: echo "lint and test passed or were skipped"
```

- `if: always()`: the gate runs even if earlier jobs failed; otherwise it
  would be skipped too, and since a skipped job counts as successful the
  PR would pass.
- `needs.*.result` is the list of the needed jobs' results. If it holds
  `failure` or `cancelled`, `exit 1` fails the gate.
- `>-` splits a long expression over lines; YAML reads it as one line.
- One name is left on the required list: `ci-ok`. Adding a new Python
  version to the matrix or renaming a job no longer breaks the rule.

## The merge queue

The "branch must be up to date" rule is tiring in a busy repository:
after every merge, all open PRs are updated with `main` and tested again.
GitHub's **merge queue** puts this in order: an approved PR enters the
queue, GitHub tests it together with the ones in front of it on a
temporary branch, and merges it if it passes.

Testing in the queue starts with a separate event: `merge_group`. If the
workflow does not listen to this event, the required checks never run in
the queue and the PR gets stuck there:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  merge_group:
```

## Checking the PR title

Many teams merge PRs with "squash": all of the PR's commits become one
commit and that commit's message is **the PR's title**. The version bump
in the tenth section looked at commit prefixes (`feat:`, `fix:`); then
the PR title must follow this rule too. Let's write the rule as a
regular expression:

```python
import re

TITLE = re.compile(r"^(feat|fix|docs|test|chore)(\([a-z-]+\))?!?: \S.*$")

for title in ["feat(login): add remember me", "Fix login bug",
              "fix: ", "feat!: drop Python 3.11"]:
    print(f"{title!r:32} {bool(TITLE.match(title))}")
```

```text
'feat(login): add remember me'   True
'Fix login bug'                  False
'fix: '                          False
'feat!: drop Python 3.11'        True
```

- `(\([a-z-]+\))?` is the optional scope: `(login)`.
- `!?` is the breaking change mark.
- `: \S.*` is a space after the colon and a non-empty summary. This is
  why `"fix: "` does not pass.

In the pipeline the check gives the PR title to a script. The rule from
the ninth section holds here too: the title is text from outside, it is
not written straight into the `run:` line, it goes into `env:`.

```yaml
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
```

```yaml
  title:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/check_title.py "$TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

`edited` in the `types` list matters: by default `pull_request` runs
only when a PR is opened, gets a new commit or is reopened. Without
`edited`, the person who fixes the title cannot run the check again.

## A warning about `pull_request_target`

There is also the `pull_request_target` event: it runs not on the PR's
code but on **the target branch's** code, with secrets and write
permission (for jobs like writing a comment on a PR from a fork). If the
PR's code is fetched and run in this event, anyone who opens a fork runs
whatever they want with your pipeline's secrets. The rule: the PR's code
is not run inside `pull_request_target`. For tests, always
`pull_request`.

## Next

In the fourteenth section we deal with **flaky tests** that sometimes
pass and sometimes fail, and with finding the cause of a failing
pipeline.

## Summary

- A branch strategy is the team's agreement; the shorter branches live,
  the easier merging is. GitHub flow: branch, PR, review, `main`.
- `main` is protected with rules: PR, approval, required checks, an
  up-to-date branch, no force pushes.
- A required check's name is the job's name; in a matrix `test (3.12)`.
  If the name changes or the workflow never starts, the PR keeps waiting.
- A skipped job counts as successful; one gate job built with
  `if: always()` + `needs.*.result` simplifies the required list.
- If a merge queue is used, the workflow also listens to `merge_group`.
- The PR title check goes through `env:`; `edited` in `types` so it runs
  again when the title is fixed.
- The PR's code is not run inside `pull_request_target`.
