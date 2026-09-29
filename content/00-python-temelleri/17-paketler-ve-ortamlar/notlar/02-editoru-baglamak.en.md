Typing `activate` in a terminal **does not affect your editor.** VS Code's
"Run" button and Jupyter's cells run with whichever Python they were told to
use. That is the most common reason for getting `ModuleNotFoundError` in the
editor while everything is fine in the terminal.

The rule: **after creating an environment, tell the editor too.**

## VS Code

First you need Microsoft's **Python** extension (search for "Python" in the
Extensions pane).

### Choosing the interpreter

1. Open the command palette with `Ctrl` + `Shift` + `P`.
2. Type **Python: Select Interpreter** and pick it.
3. Choose the project's environment: `('.venv': venv)` for `.venv`, or the
   environment's name for conda.

The chosen interpreter is shown in the bottom-right corner of the window.
Click it to choose again.

If the `.venv` in the project folder is not in the list, use **Enter
interpreter path** and point at the file directly:

```text
.venv\Scripts\python.exe
```

### Creating the environment from VS Code

**Python: Create Environment** in the command palette: pick `Venv` or
`Conda`, pick the Python version; if there is a `requirements.txt` it offers
to install that too. The result is the same as the commands you would type
in a terminal.

### VS Code's terminal

After you choose the interpreter, every **new** terminal you open in VS Code
activates the environment on its own; `(.venv)` appears at the start. A
terminal opened before the choice stays as it was: close it and open a new
one.

## Jupyter

In Jupyter, what runs the cells is called the **kernel**. A kernel is a
Python interpreter; it sees the packages of whichever environment it lives
in.

### Registering an environment as a kernel

With the environment active:

```text
python -m pip install ipykernel
python -m ipykernel install --user --name project-a --display-name "Project A"
```

"Project A" now appears in Jupyter's kernel list. To see and remove
registered kernels:

```text
jupyter kernelspec list
jupyter kernelspec uninstall project-a
```

When you open a notebook (`.ipynb`) in VS Code, choose the environment with
the **Select Kernel** button at the top right; if `ipykernel` is missing, VS
Code offers to install it. In browser Jupyter use **Kernel → Change Kernel**.

### Installing packages from a notebook

Write `%pip` in a cell, not `!pip`:

```text
%pip install pandas
```

`%pip` installs into the environment of **the kernel running the notebook**.
`!pip` runs a terminal command and goes to whichever pip comes first on
`PATH`; the package may end up in a different Python. The same applies in a
conda environment: `%conda install`.

Restart the kernel (**Restart**) afterwards; a running kernel does not always
see the new package straight away.

## PyCharm

**Settings → Project → Python Interpreter → Add Interpreter**: here you can
create a new `Virtualenv` environment or pick an existing `.venv` or conda
environment. PyCharm usually creates a `.venv` on its own for a new project.

## Which Python am I in?

Whatever the editor says, the code gives the answer. Put this in a cell or a
file:

```python
import sys
print(sys.executable)
```

If the path does not point at the project's environment
(`...\project-a\.venv\Scripts\python.exe` or `...\envs\project-a\python.exe`),
the editor is on the wrong interpreter.
