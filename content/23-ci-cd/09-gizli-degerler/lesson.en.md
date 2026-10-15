# Secrets and Security

So far our pipeline has only worked within itself: it got the code,
tested it, packaged it. The next step is talking to the outside world:
uploading the package to a repository, deploying to a server, sending a
report to a service. All of these need a **password** or a **key**. In
this section we look at two things: how the pipeline uses these keys
safely, and how the pipeline itself can turn into a door for an attack.

## Why is a key not written in the code?

The secret text a service gives you so it can recognise you is called an
**API key**. Whoever knows the key can send requests to that service in
your name. The easiest place for it is the code, and that is also the
most dangerous one:

- Everyone who can see the repository sees the key. For a public
  repository, that means the whole internet.
- Deleting the line later is not enough. Git keeps old commits; the key
  stays in the **history**.

Let's see the second point with a small model. We keep three versions of
a file in a list (each one a commit); the key was written in the first
version and deleted in the second:

```python
import re

API_KEY = re.compile(r"apikey_[A-Za-z0-9]{20}")

history = [
    'URL = "https://api.example.com"\nKEY = "apikey_7Hq2Lm9Xc4Vb8Nz1Rt5W"\n',
    'URL = "https://api.example.com"\nKEY = os.environ["KEY"]\n',
    'URL = "https://api.example.com/v2"\nKEY = os.environ["KEY"]\n',
]

print("today:  ", bool(API_KEY.search(history[-1])))
for number, version in enumerate(history, start=1):
    if API_KEY.search(version):
        print("commit", number, "still has the key")
```

```text
today:   False
commit 1 still has the key
```

Today's file has no key, but whoever looks at the first commit finds it.
Real tools (like GitHub's secret scanning) do exactly this: they search
the whole history for known key formats. That is why the rule is: **once
a key has entered the repository, treat it as leaked.** What you need is
not deleting it but **getting a new one from the service and revoking the
old one** (rotation).

## Secrets on GitHub

The key's place is not the repository but GitHub's **secret** store: on
the repository's **Settings › Secrets and variables › Actions** page you
enter a name and a value. The value is stored encrypted; once saved, it
is not shown even on that page, it can only be changed. Names contain
letters, digits and underscores; they cannot start with a digit or with
`GITHUB_`.

In a workflow the value is reached with `${{ secrets.NAME }}`. It is best
given as an environment variable (`env:`) only to the step that needs it:

```yaml
name: Report

on:
  push:
    branches: [main]

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python send_report.py
        env:
          REPORT_API_KEY: ${{ secrets.REPORT_API_KEY }}
```

On the Python side the code reads the key from the environment and knows
nothing itself: `os.environ["REPORT_API_KEY"]`. The same code runs on
your computer with your own key and in the pipeline with the key from the
store.

For settings that are not secret (an address, a region name) the same
page has **variables**: `${{ vars.NAME }}`. A variable shows up openly in
the logs; a password does not go into one.

## Masking in the log

If a step prints a secret by mistake, GitHub replaces it with `***` in
the log. That is a nice safety belt, but you need to know how it works:
it looks for the **exact** value in the log text. With a simplified
model:

```python
import base64


def mask(line, secrets):
    for secret in secrets:
        line = line.replace(secret, "***")
    return line


secret = "s3cr3t-Token-42"
print(mask("Connecting with s3cr3t-Token-42", [secret]))

encoded = base64.b64encode(secret.encode()).decode()
print(mask("Header: " + encoded, [secret]))
```

```text
Connecting with ***
Header: czNjcjN0LVRva2VuLTQy
```

Written exactly, the value was hidden. But once the same value was turned
into base64 (a step may have converted it to put it in a header), it was
a different text and went into the log as it is. Base64 is not
encryption; anyone who sees the log can turn it back. Two rules follow:

- Do **not** print a secret; do not say "it gets hidden anyway" and rely
  on masking.
- If a step derives a new secret from a value, it adds it to the list of
  values to mask itself: `echo "::add-mask::$TOKEN"`.

## A PR from a fork

In a public repository anyone can take a copy of the repository (a fork)
and open a PR. That PR's code runs in your pipeline. If the secrets were
given to it, someone with bad intentions would add a "send the key
somewhere" step to the workflow and open a PR. That is why GitHub **does
not give secrets to PRs from forks**: `${{ secrets.NAME }}` comes in
empty. Only the `GITHUB_TOKEN` we are about to see comes, and only with
read access.

The consequence: steps that need secrets (deploying, releasing) run not
in a PR but on a push to `main` or when a tag arrives. In a PR only tests
and checks run.

## `GITHUB_TOKEN` and permissions

GitHub gives every run a temporary key by itself: `GITHUB_TOKEN`. With it
the pipeline can write something to the repository (a tag, a release, a
PR comment). It stops being valid when the run ends. What it can do is
set by **permissions** (`permissions:`); the default permissions can be
broad, depending on the repository's setting.

The basic principle of security applies here too: **least privilege**.
Each job gets only as much permission as it really needs. If an action
running in the pipeline is taken over, the damage is as large as the
permissions.

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest
  release:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: gh release create "$GITHUB_REF_NAME" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- The `permissions:` at the top is the default for all jobs: read only.
- The `release` job overrides it with its own `permissions:` block: it
  asks for `contents: write` to create a release. The `test` job stays
  on read.
- Once `permissions:` is written, **every permission not in the list is
  closed** (`none`). Adding a permission is a deliberate act.

<figure class="fig anat">
  <div class="anat-row"><span><code>contents</code></span><span>The repository's files, tags, releases.</span></div>
  <div class="anat-row"><span><code>pull-requests</code></span><span>Writing a comment on a PR, adding a label.</span></div>
  <div class="anat-row"><span><code>packages</code></span><span>GitHub's package and image registry.</span></div>
  <div class="anat-row"><span><code>id-token</code></span><span>A short-lived identity for logging in to a cloud without a password.</span></div>
</figure>

Each one takes `read`, `write` or `none`.

## Actions are someone else's code

When you write `uses: actions/checkout@v4`, you run another repository's
code, with your permissions, on a machine that can reach your secrets.
`@v4` is a **tag**, and a tag can move: the action's owner (or someone
who takes over their account) can point `v4` at a completely different
commit, and your pipeline runs that code on its next run.

There are two precautions:

- Use actions from sources you trust (GitHub's own `actions/` actions,
  well-known organisations).
- In critical pipelines pin the action not by a tag but by a **commit
  id**: `actions/checkout@` followed by the 40-character commit id, with
  the version it is as a comment at the end of the line (`# v4`). A
  commit id cannot be changed. You update it by hand or with a tool like
  Dependabot.

## Code injection

`${{ ... }}` expressions are written into the text **before** the shell
runs. If the expression's value is text that comes **from outside**, like
a PR title, a branch name or a comment, the person who wrote it has
written part of the command. Let's see how a PR title gets mixed into the
command. We count how many pieces the command splits into with Python's
`shlex` module (`;` separates two commands in the shell):

```python
import shlex


def commands(line):
    tokens = list(shlex.shlex(line, posix=True, punctuation_chars=True))
    return tokens.count(";") + 1


unsafe = 'echo "PR title is ${{ github.event.pull_request.title }}"'
title = 'Fix typo"; echo leaked=$API_KEY; echo "'
rendered = unsafe.replace("${{ github.event.pull_request.title }}", title)
print(rendered)
print("commands:", commands(rendered))

safe = 'echo "PR title is $TITLE"'
print(safe)
print("commands:", commands(safe))
```

```text
echo "PR title is Fix typo"; echo leaked=$API_KEY; echo ""
commands: 3
echo "PR title is $TITLE"
commands: 1
```

The quote in the title closed `echo`'s text, and everything after it
became a separate command: the person who opened the PR can run any
command they like in your pipeline. In the safe form the title is put
into an **environment variable** and the command only contains the
variable's name. When the shell puts in the variable's value, it does not
read it again as a command; whatever is inside, it is a single text:

```yaml
      - run: echo "PR title is $TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

The rule: a value from outside is not written into a `run:` line directly
with `${{ }}`; it is first put into `env:`.

## Next

We have seen how to keep keys safe and narrow down permissions. In the
tenth section we release the package with a version number: a pipeline
that runs when a tag arrives, creates a release with the
`contents: write` permission and uploads the package with a secret.

## Summary

- A key is not written in the code; if it was, deleting it is not
  enough, git history keeps it. A leaked key is revoked and replaced.
- A secret lives in the repository's store, is read with
  `${{ secrets.NAME }}` and is given with `env:` only to the step that
  needs it. A setting that is not secret is `${{ vars.NAME }}`.
- Masking in the log hides only the exact value; a transformed value
  leaks. A secret is not printed.
- PRs from forks get no secrets.
- `GITHUB_TOKEN` is every run's temporary key; `permissions:` gives it
  least privilege. Read at the top, write in the job that needs it.
- An action is someone else's code; in a critical pipeline it is pinned
  by a commit id.
- Text from outside is not written straight into `run:`; it is passed
  through `env:`.
