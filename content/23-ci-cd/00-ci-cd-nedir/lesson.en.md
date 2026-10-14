# What CI/CD Is

Writing a program is half of the job. The other half is making sure that
every change you make does not break the program, and getting the program
to its users. The first module of this path is about that second half:
building a **pipeline** that runs by itself on every change, tests the
code, checks it, packages it and releases it. In this section we look at
what a pipeline is, why it is needed and which parts it is made of; you
also write your first workflow file.

## "It worked on my machine"

Picture a team of three. Everyone works on their own computer, on their
own branch (the **branch** from the Git path). After two weeks they merge
their work into the main branch, and this happens:

- Ayşe changed a function, and Mert's code still calls it the old way.
  Both of them had passed the tests on their own computers.
- Selin installed a new package but forgot to add it to
  `requirements.txt`. The program only works on her computer.
- Making a release takes ten commands. Someone skips one step, and users
  get a version whose tests were never run.

None of these problems comes from bad programming. They share one cause:
**merging is rare, checking is manual and everyone's computer is
different.** The later a mistake is found, the more it costs, because two
weeks later the answer to "which change broke this?" is lost among
hundreds of lines.

## Continuous integration (CI)

**Integration** means adding everyone's changes to the shared code, in
other words merging. **Continuous integration** (**CI** for short) means
doing that often and in small pieces instead of rarely and in big ones.
But what really makes CI is the second half: **every time a change
arrives, the code is installed and tested automatically.**

So CI is made of two habits:

1. Keep changes small and merge them often (several times a day).
2. On every merge, let a machine install the code from scratch in a
   **clean environment** and run all the tests. The result arrives within
   a few minutes.

The "clean environment" matters: the tests run not on your computer but
on a machine where nothing is installed in advance. The package Selin
forgot is not there, the test fails at once and the problem shows up long
before merge day.

## Continuous delivery and continuous deployment (CD)

The abbreviation **CD** is used as the name of two different things, so
let us separate them:

- **Continuous delivery:** every change that passes the tests is turned
  automatically into a **package that is ready to release**. Releasing is
  as easy as pressing one button, but a person presses it.
- **Continuous deployment:** there is no button either. Every change that
  passes the tests reaches the users automatically.

<figure class="fig versus">
  <div class="no"><h4>Manual release</h4>The steps live in a document or in someone's head. One of them can be skipped. Releases are rare and big; when one breaks, finding the cause is hard.</div>
  <div class="ok"><h4>CI/CD pipeline</h4>The steps are written in a file and run in the same order every time. Releases are frequent and small; the failing step tells you at once which change is the problem.</div>
  <figcaption>The difference is not in the code itself but in its journey.</figcaption>
</figure>

Which one you choose depends on the risk. A website can update itself
several times a day; a bank's payment system, or a program installed on
the user's computer, is usually released after a person's final approval.
Odyssey itself is of the second kind: when a new release tag is pushed, a
workflow checks the content, builds the program and prepares the
installer, but a person still decides when to publish the release. That
is continuous delivery.

## The pipeline: stages and gates

The ordered list of steps in the code's journey is called a **pipeline**.
The pipeline of a typical Python project looks like this:

<figure class="fig">
  <div class="flow">
    <span class="node">Install</span>
    <span class="arrow">→</span>
    <span class="node">Check</span>
    <span class="arrow">→</span>
    <span class="node acc">Test</span>
    <span class="arrow">→</span>
    <span class="node">Package</span>
    <span class="arrow">→</span>
    <span class="node">Release</span>
  </div>
  <figcaption>Every stage is a gate: if it fails, the later stages do not run.</figcaption>
</figure>

- **Install:** download the code, install Python and the dependencies.
- **Check:** look at the style of the code and at common mistakes (in the
  code quality gates section).
- **Test:** run the automated tests (the next section).
- **Package:** produce the file that goes to the users.
- **Release:** deliver the package to the users.

The most important rule of a pipeline: **if a stage fails, the pipeline
stops there.** Code that does not pass the tests is not packaged, and code
that is not packaged is not released. This is called **failing fast**:
catching a problem as early and as cheaply as possible. That is why fast
stages (a style check takes a few seconds) go before slow ones (long
tests, building).

Let us see this rule in a small imitation in Python. Each stage is a
function; it returns `True` if it passed and `False` if it failed:

```python
def install():
    print("install: ok")
    return True


def lint():
    print("lint: ok")
    return True


def test():
    print("test: 1 of 12 tests failed")
    return False


def package():
    print("package: ok")
    return True


pipeline = [("install", install), ("lint", lint), ("test", test), ("package", package)]

passed = True
for name, stage in pipeline:
    if not stage():
        print("pipeline stopped at:", name)
        passed = False
        break
if passed:
    print("pipeline passed")
```

```text
install: ok
lint: ok
test: 1 of 12 tests failed
pipeline stopped at: test
```

`package` never ran: the pipeline stopped the moment the test failed.
This is exactly what happens in a real CI service. The failed stage is
marked in red on the screen, and the person who sent the change is told.

The result of a pipeline is described with one word: **green** (green
build) if it passed, **red** (red build) if it failed. The most important
team rule comes from this: **if the main branch is red, fix it first**;
nobody adds new work on top of it.

## Who runs the pipeline?

A **CI service** runs the pipeline. In this path we use **GitHub
Actions**, GitHub's service, because your code already lives on GitHub
(the Git path) and it is one of the most widely used. The ideas are the
same in other services; only the way the file is written changes.

A few terms:

- **Workflow:** the file that describes the pipeline. It is a YAML file
  inside the repository, in the `.github/workflows/` folder (the same
  language as `compose.yaml` in the Docker path).
- **Trigger:** the event that starts the workflow. For example "when
  someone does a `push`".
- **Job:** a group of steps that run on the same machine.
- **Step:** a single command or a ready-made action.
- **Runner:** the machine that runs the job. It is a clean virtual
  computer started from scratch for every run and deleted when the job
  ends.

## Your first workflow file

The smallest useful workflow looks something like this:

```yaml
name: CI

on: push

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

Line by line:

<figure class="fig anat">
  <div class="anat-row"><span><code>name: CI</code></span><span>The name of the workflow; this is how it appears in the list on GitHub.</span></div>
  <div class="anat-row"><span><code>on: push</code></span><span>The trigger: run on every <code>push</code> to the repository.</span></div>
  <div class="anat-row"><span><code>jobs:</code></span><span>The list of jobs. Here there is one job: <code>test</code>.</span></div>
  <div class="anat-row"><span><code>runs-on</code></span><span>The machine the job runs on: the latest version of Ubuntu Linux.</span></div>
  <div class="anat-row"><span><code>steps:</code></span><span>The steps, run in order. Each step starts with <code>-</code>.</span></div>
  <div class="anat-row"><span><code>uses:</code></span><span>Use a ready-made action. <code>actions/checkout@v4</code> downloads the repository's code to the machine; <code>@v4</code> is the version of the action.</span></div>
  <div class="anat-row"><span><code>with:</code></span><span>Settings given to the action: which Python version to install.</span></div>
  <div class="anat-row"><span><code>run:</code></span><span>Run a command, just as you would type it in a terminal.</span></div>
</figure>

Because the machine is clean, the first step is always downloading the
code: the repository's code is not on the runner by itself. Forgetting
this is one of the most common mistakes; the later steps run in an empty
folder and `requirements.txt` cannot be found.

We open up every part of the file one by one in the Anatomy of a
Workflow File section. For now it is enough to know the shape: **when**
(`on`), **where** (`runs-on`), **what** (`steps`).

## How we work in this module

Odyssey runs offline and does not connect to a real CI service. So there
are two kinds of exercises:

- **Workflow exercises:** you write the `.github/workflows/ci.yml` file.
  The file is not run; it is **checked** against GitHub's rules: is the
  structure right (does every job have a `runs-on`, are the action
  versions written), are the requested trigger, steps and order there.
  The check catches the mistakes GitHub would reject, but it cannot
  measure what the file would do on a real machine. You can try it for
  real in your own repository: the file runs as soon as you push it to
  GitHub.
- **Python exercises:** the tests and the code that runs inside the
  pipeline are really run; every result here is a measured result.

## Summary

- **CI:** merge changes often; on every merge the code is installed and
  tested automatically on a clean machine.
- **Continuous delivery:** every change that passes the tests becomes a
  package ready to release; a person starts the release. **Continuous
  deployment:** the release is automatic too.
- A **pipeline** is made of stages; if a stage fails, the pipeline stops.
  Fast stages go first (failing fast).
- In GitHub Actions the pipeline is described by a **workflow** file:
  `on` (when), `jobs` → `runs-on` (where), `steps` (what).
