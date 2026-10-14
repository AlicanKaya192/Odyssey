# The Anatomy of a Workflow File

In the first section we saw the skeleton of a workflow file: **when**
(`on`), **where** (`runs-on`), **what** (`steps`). In this section we open
the file up piece by piece: the rules of YAML, the settings a job and a
step can take, multi-line commands, environment variables and the traps
people often fall into with YAML.

## The three rules of YAML

A workflow file is written in **YAML**. YAML is a format designed to
write nested data with few symbols. Three rules carry the whole file:

1. **Key and value:** `runs-on: ubuntu-latest`. A space after the colon.
2. **List:** each item starts with `-`. The steps are a list.
3. **Indentation shows nesting:** everything under a key starts further
   in than the key. Indentation is done with **spaces**; the tab character
   is not used. Usually two spaces.

Let us see how Python's YAML reader (PyYAML) reads a workflow. We print
the result as JSON so it is easier to read:

```python
import json

import yaml

text = """
name: CI
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest
"""
data = yaml.safe_load(text)
print(json.dumps(data, indent=2))
```

```text
{
  "name": "CI",
  "jobs": {
    "test": {
      "runs-on": "ubuntu-latest",
      "steps": [
        {
          "uses": "actions/checkout@v4"
        },
        {
          "run": "python -m pytest"
        }
      ]
    }
  }
}
```

The file is a **tree of dictionaries and lists**: `jobs` is a dictionary,
`test` inside it is a dictionary, its `steps` is a list, and each item of
the list is a dictionary again. GitHub reads the file as this tree too.
Shifting the indentation by one space moves a key to another branch of
the tree; that is why indentation mistakes are the most common YAML
mistakes.

## The top level of the file

<figure class="fig anat">
  <div class="anat-row"><span><code>name</code></span><span>The name of the workflow. It appears in the list on GitHub. If it is missing, the file path appears instead.</span></div>
  <div class="anat-row"><span><code>on</code></span><span>The triggers: which events start the workflow (the fourth section).</span></div>
  <div class="anat-row"><span><code>env</code></span><span>Environment variables valid in every job.</span></div>
  <div class="anat-row"><span><code>jobs</code></span><span>The jobs. Each job's name is its own key (<code>test</code>, <code>lint</code>...).</span></div>
</figure>

A repository can have several workflow files; every `.yml` or `.yaml` file
in the `.github/workflows/` folder is a separate workflow.

## A job

Every job runs on its own clean machine. Common settings:

<figure class="fig anat">
  <div class="anat-row"><span><code>runs-on</code></span><span>The machine: <code>ubuntu-latest</code>, <code>windows-latest</code> or <code>macos-latest</code>. Required.</span></div>
  <div class="anat-row"><span><code>name</code></span><span>The name shown on the screen (it can differ from the job's key).</span></div>
  <div class="anat-row"><span><code>env</code></span><span>Environment variables valid only in this job's steps.</span></div>
  <div class="anat-row"><span><code>timeout-minutes</code></span><span>If the job takes longer than this many minutes it is stopped, so a stuck test does not keep the pipeline busy for hours.</span></div>
  <div class="anat-row"><span><code>steps</code></span><span>The list of steps. Required.</span></div>
</figure>

The choice of machine also changes how commands run: on Linux and macOS
machines `run` commands run in the **bash** shell, on the Windows machine
in **PowerShell**. The same command can behave differently in the two
shells; that is why most projects run their tests on Linux.

## A step

<figure class="fig anat">
  <div class="anat-row"><span><code>name</code></span><span>The name of the step on the screen. It makes it easier to find which step failed in the logs.</span></div>
  <div class="anat-row"><span><code>uses</code></span><span>A ready-made action, with its version: <code>actions/checkout@v4</code>.</span></div>
  <div class="anat-row"><span><code>with</code></span><span>Settings given to the action.</span></div>
  <div class="anat-row"><span><code>run</code></span><span>The command or commands to run.</span></div>
  <div class="anat-row"><span><code>env</code></span><span>Environment variables valid only in this step.</span></div>
  <div class="anat-row"><span><code>working-directory</code></span><span>Which folder the <code>run</code> command runs in.</span></div>
</figure>

A step has either `uses` or `run`, never both.

## A multi-line command

To run several commands in one step, write `run: |`. The `|` sign means
"take the lines below as they are"; each line runs in order, and if one
fails the step fails:

```yaml
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
```

## Environment variables and their levels

An **environment variable** is a named value given to programs from the
outside. It is the same idea as `-e` and `environment:` in the Docker
path. In a workflow it can be written at three levels:

<figure class="fig versus">
  <div><h4>Workflow</h4><code>env:</code> at the top level. Valid in every job and step.</div>
  <div><h4>Job</h4><code>env:</code> under the job. Valid in all of that job's steps.</div>
  <div><h4>Step</h4><code>env:</code> under the step. Valid only in that step.</div>
  <figcaption>If the same name is written at several levels, the one closest to the step wins.</figcaption>
</figure>

Inside a `run` command a variable is read with the shell's syntax: in
bash, `$APP_ENV`. Outside the command, for example in a `with` value, the
workflow's **expression** syntax is used: `${{ env.APP_ENV }}`. We will see
expressions often in the coming sections.

All of it together:

```yaml
name: CI

on: push

env:
  APP_ENV: ci

jobs:
  test:
    name: Run the tests
    runs-on: ubuntu-latest
    timeout-minutes: 10
    env:
      APP_ENV: test
    steps:
      - name: Get the code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest
        env:
          PYTEST_ADDOPTS: "-q"
```

In the steps of the `test` job, `APP_ENV` is `test`: the job-level value
overrides the workflow-level one. `PYTEST_ADDOPTS` exists only in the last
step.

## YAML traps

Because YAML is written with few symbols, some values are not read as the
type you expect. We measured with PyYAML:

```python
import yaml

print(yaml.safe_load("version: 3.10"))
print(yaml.safe_load('version: "3.10"'))
print(yaml.safe_load("on: push"))
```

```text
{'version': 3.1}
{'version': '3.10'}
{True: 'push'}
```

- **`3.10` is read as a number and becomes `3.1`.** That is why writing
  the Python version without quotes asks for Python 3.1. Always write
  versions in quotes: `"3.10"`.
- **The word `on`** is read as `True` by PyYAML (the rules of version 1.1
  of YAML). GitHub's own reader understands `on` correctly; but if you
  write your own tool that processes workflow files with Python, you have
  to take this into account.

And the tab character:

```python
import yaml

try:
    yaml.safe_load("jobs:\n\ttest: 1")
except yaml.YAMLError as error:
    print(type(error).__name__)
    print(error.problem)
```

```text
ScannerError
found character '\t' that cannot start any token
```

Pay attention to whether your editor writes spaces or a tab when you
press the Tab key; Odyssey's editor writes spaces.

## A run on GitHub

Once the file is pushed to the repository, it appears in the repository's
**Actions** tab on GitHub. Each run is one row; inside it the jobs are
listed, and inside each job the steps. Each step's log opens separately;
the failed step is marked in red and the error message is at the end of
its log. This is where giving steps a `name` really pays off: seeing that
the "Run tests" step failed is easier than looking for a "Run python -m
pytest" line.

## Summary

- YAML: `key: value`, lists with `-`, nesting with space indentation. The
  file is a tree of dictionaries and lists.
- Top level: `name`, `on`, `env`, `jobs`. Job: `runs-on`, `name`, `env`,
  `timeout-minutes`, `steps`. Step: `name`, `uses` + `with` or `run`,
  `env`, `working-directory`.
- `run: |` runs several commands in order.
- Environment variables at three levels; the one closest to the step wins.
- Write versions in quotes (`"3.10"`); do not indent with tabs.
