`math` and `datetime` ship with Python. But `pandas`, `numpy` and `requests`
do not — you have to install those.

This note covers that job. It will be the first thing you do when you move on
to the Data Science path.

## What is `pip`?

`pip` is Python's package manager. It is installed along with Python. You type
into a terminal:

```bash
pip install pandas
```

It downloads the library from the internet and installs it on your machine.
Then you can use it in your code:

```python
import pandas
```

The commands you will use often:

| Command | What it does |
|---|---|
| `pip install name` | Installs it |
| `pip install name==2.1.0` | Installs a particular version |
| `pip install --upgrade name` | Upgrades it |
| `pip uninstall name` | Removes it |
| `pip list` | Lists what is installed |
| `pip show name` | Shows its version and where it was installed |

## Where is the terminal?

- **Windows:** type `cmd` or `powershell` into the Start menu.
- **Inside VS Code:** `Ctrl` + `` ` `` (the backtick key).

If the command does not work, try this instead of `pip`:

```bash
python -m pip install pandas
```

That form is more reliable: it means "use the `pip` belonging to the
interpreter I am calling `python` right now". It matters when there is more
than one Python on the machine.

## The real issue: virtual environments

There is a problem. When you install libraries directly, they all go to **the
same place**:

<figure class="fig">
  <div class="flow">
    <span class="node no"><b>Project A</b><br>wants pandas 1.5</span>
    <span class="arrow">→</span>
    <span class="node"><b>One Python</b><br>one pandas version</span>
    <span class="arrow">←</span>
    <span class="node no"><b>Project B</b><br>wants pandas 2.1</span>
  </div>
  <figcaption>When two projects want different versions, installing for one breaks the other. A virtual environment gives each project its own library folder.</figcaption>
</figure>

A **virtual environment** is a separate Python installation that lives inside
the project folder. Everything you install for that project goes there and
does not affect anything outside.

### Creating one

In the project folder:

```bash
python -m venv .venv
```

A folder called `.venv` appears. The project's own Python lives inside it.

### Activating it

```bash
.venv\Scripts\activate
```

`(.venv)` appears at the start of the terminal line — you are now inside that
environment. From then on, everything you `pip install` goes there.

To leave:

```bash
deactivate
```

### Why every time?

When you open a new terminal the environment is not active. You have to
activate it again. VS Code usually finds and selects the `.venv` in the folder
by itself.

## `requirements.txt`

You keep a record of which libraries the project uses in a file:

```
pandas==2.1.0
numpy==1.26.0
```

Writing what is installed into that file:

```bash
pip freeze > requirements.txt
```

Installing all of it on another machine:

```bash
pip install -r requirements.txt
```

This stops whoever you share the project with from having to ask "which
libraries did this need?"

## Common errors

**`ModuleNotFoundError: No module named 'pandas'`**

The library is not installed, or it is installed in **the wrong environment**.
Activate the environment first, then install. That is the most common cause:
the install happens in one terminal and the run happens in another
environment.

**`pip is not recognized`**

`pip` is not on the path. Use the `python -m pip install ...` form.

**`Permission denied`**

You are trying to install into the system Python. Create a virtual
environment and the problem goes away. Running as administrator also works,
but it is **not the right fix** — it pollutes the system Python.

## Summary

- Everything outside the standard library is installed with `pip install`.
- If the command fails, `python -m pip install` is more reliable.
- **Create a virtual environment for every project.** It is the only answer
  when two projects want different versions.
- `python -m venv .venv` creates one and `.venv\Scripts\activate` activates
  it.
- `requirements.txt` records what the project needs.
- `ModuleNotFoundError` usually means "you are in the wrong environment".
