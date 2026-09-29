Almost every setup error comes down to one of two questions: **which Python
is running** and **which Python the package was installed into**. For each
error below, check those first.

## `ModuleNotFoundError: No module named 'pandas'`

The code runs but cannot find the package. Either it was never installed or
it went into **a different Python**. In order:

1. Which Python does the code run in?
   `import sys; print(sys.executable)`
2. Which Python does the terminal run? `where python`
3. Is the package in that Python? `python -m pip show pandas`

If the paths do not match: activate the right environment (or choose the
right interpreter in your editor) and install **there** with
`python -m pip install pandas`.

In a notebook the kernel may be a different environment; run
`%pip install pandas` in a cell, then restart the kernel.

## The install name differs from the import name

`pip install sklearn` fails, or `import scikit_learn` is not found. For some
packages the name on PyPI is not the name in code:

| To install | In code |
|---|---|
| `scikit-learn` | `import sklearn` |
| `opencv-python` | `import cv2` |
| `Pillow` | `import PIL` |
| `beautifulsoup4` | `import bs4` |
| `python-dateutil` | `import dateutil` |
| `PyYAML` | `import yaml` |

If unsure, look at the package's PyPI page or the first page of its
documentation.

## `'pip' is not recognized...` / `pip: command not found`

The `pip` command is not on `PATH`. The fix should already be your habit:

```text
python -m pip install pandas
```

If `python` is not recognised either, **Add python.exe to PATH** was not
ticked during installation. Run the installer again and add it with
"Modify", or use the `py` launcher on Windows: `py -m pip install pandas`.

## Typing `python` opens the Microsoft Store

Windows' own "app execution aliases" send the `python` command to the Store.
Under **Settings → Apps → Advanced app settings → App execution aliases**,
turn off the `python.exe` and `python3.exe` entries.

## PowerShell: "running scripts is disabled on this system"

`.venv\Scripts\Activate.ps1` does not run because PowerShell does not run
scripts by default. To allow it for your own user only:

```text
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

If you would rather not, use `.venv\Scripts\activate` in a `cmd` window, or
skip activating and work with `.venv\Scripts\python`.

## `conda: The term 'conda' is not recognized`

conda has not been introduced to a normal PowerShell. Use the **Anaconda
Prompt** window, or run `conda init powershell` once (in the Anaconda Prompt)
and reopen the terminal.

## `error: externally-managed-environment`

This appears when you `pip install` into Homebrew's Python on macOS or the
system Python on Linux. The operating system wants to protect its own Python.
The fix is a virtual environment:

```text
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas
```

Do not use the `--break-system-packages` flag suggested online; its name says
what it does.

## `Access is denied` / `Permission denied`

You are installing somewhere you have no right to, usually the Python shared
by all users. Running the terminal as administrator works but is not the
right fix: it pollutes the system's Python. Create a virtual environment; it
lives in your own folder, so the permission problem goes away.

## `No matching distribution found for ...`

pip could not find the package. Three likely reasons:

- The name is misspelled (see the table above too).
- The version you asked for does not exist, like `pandas==9.0`.
- There is no ready-made build of the package **for your Python version**.
  This is common with a very new Python release; create the environment with
  a Python version from a few months earlier (`py -3.12 -m venv .venv`).

## `ResolutionImpossible` / "conflicting dependencies"

The versions you asked for do not fit together: package A wants `numpy<2`,
package B wants `numpy>=2`. Loosen exact pins (`==`) in `requirements.txt` to
`>=` and let pip look for a combination that works. If that fails you may
need to split the two packages into separate environments.

## A strange file called `=2.0` in the folder

You typed `python -m pip install pandas>=2.0` and the terminal read `>` as
"write to a file". Delete the file and quote the version: `"pandas>=2.0"`.

## I moved the project folder and the environment stopped working

`Fatal error in launcher: Unable to create process`, or the wrong Python after
`activate`. The environment has the old full paths written inside. Delete it
and create it again:

```text
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## `AttributeError: partially initialized module 'pandas'`

You named your file `pandas.py` (or `random.py`, `math.py`, `numpy.py`). When
you write `import pandas`, Python finds the file in **your own folder** first
and imports it instead of the real library. Rename the file and delete the
`__pycache__` folder that appeared next to it.

## Two environments in the prompt: `(.venv) (base)`

Both conda's `base` and your `.venv` are active. Which Python runs becomes
unclear. Close one of them; if you do not want `base` every time a terminal
opens:

```text
conda config --set auto_activate_base false
```
