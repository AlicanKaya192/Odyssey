# Packages and Environments

You do not need to install anything to write code in this app; the exercises
run inside it. But the day you open your first project on your own computer,
the first obstacle is usually not the code itself. It is the **setup**:

- The `pip` command is not recognised.
- You get `ModuleNotFoundError` for a library you just installed.
- A project that runs on a friend's computer does not run on yours.

All three have the same cause: not knowing **which Python is running, with
which packages**. That is exactly what this chapter is about. You should know
the commands here by heart; you will use them in every project you open on
your own computer.

If you have not written a single line of Python yet, do not worry. There is
no coding in this chapter. It is about how Python lives on your computer. The
short list of commands is in the "Command Sheet" note.

## A few words first

<figure class="fig anat">
  <div class="anat-row"><span>Interpreter</span><span>The program that reads and runs your code. On Windows it is <code>python.exe</code>. When you say "I installed Python", this is what you installed.</span></div>
  <div class="anat-row"><span>Module</span><span>A single <code>.py</code> file. It can be brought into another file with <code>import</code>.</span></div>
  <div class="anat-row"><span>Package</span><span>A folder that groups modules together. pandas is a package with hundreds of modules inside.</span></div>
  <div class="anat-row"><span>Library</span><span>In everyday speech the same as a package: ready-made code someone else wrote and shared.</span></div>
  <div class="anat-row"><span>PyPI</span><span>The Python Package Index (<code>pypi.org</code>). The shared store of hundreds of thousands of packages. <code>pip</code> downloads from here.</span></div>
  <div class="anat-row"><span>Environment</span><span>An interpreter together with every package installed for it. The real subject of this chapter.</span></div>
  <figcaption>If you can tell these six words apart, the rest of the chapter is easy.</figcaption>
</figure>

## Which Python do you have?

Open a terminal (type `cmd` or `powershell` in the Start menu) and try:

```text
python --version
where python
```

The first shows the version, the second shows **which file** runs when you
type `python`. On macOS and Linux use `which python` instead of `where`.

`where python` may print more than one line. That is not unusual: Python may
have come from python.org, the Microsoft Store, Anaconda or from inside some
other program. **The one that runs is the first line.** Windows searches a
list of folders called `PATH` in order and runs the first `python.exe` it
finds.

On Windows the python.org installer also brings the `py` launcher. It lists
every installed version:

```text
py --list
py -3.12 --version
```

`py -3.12` means "run 3.12, whichever one comes first in the list".

## pip: the package manager

`pip` is the package manager that comes with Python. It downloads a package
from PyPI and installs it:

```text
python -m pip install pandas
```

That command does three things:

1. Downloads pandas from PyPI.
2. Finds and installs the **other packages** pandas needs (NumPy,
   python-dateutil and so on). These are called **dependencies**.
3. Puts all of them in the `site-packages` folder of the Python that ran the
   command.

The third point is the most important sentence in this chapter: **a package
is installed into the Python that installed it.** Another Python does not see
it.

### Why `python -m pip` and not just `pip`?

Most examples online simply write `pip install pandas`. With a single Python
the two are the same. With more than one, the `pip` command may belong to
**a different Python** that comes first on `PATH`. The package goes to one
place, your code runs from another, and you get `ModuleNotFoundError`.

`python -m pip` means "run the pip of the interpreter I call `python` right
now". There is no doubt left about where the package goes. **Make a habit of
always writing it this way.**

### The pip commands you will use most

| Command | What it does |
|---|---|
| `python -m pip install pandas` | Installs (with its dependencies) |
| `python -m pip install pandas==2.2.2` | Installs exactly this version |
| `python -m pip install --upgrade pandas` | Upgrades to the newest version |
| `python -m pip uninstall pandas` | Removes it |
| `python -m pip list` | Lists installed packages |
| `python -m pip show pandas` | Shows the version, where it lives, what it depends on |
| `python -m pip freeze` | Prints installed packages as `name==version` |
| `python -m pip install -r requirements.txt` | Installs everything in the file |

### Writing versions

| Written as | Meaning |
|---|---|
| `pandas==2.2.2` | Exactly 2.2.2 |
| `pandas>=2.0` | 2.0 or newer |
| `pandas>=2.0,<3.0` | Anything in the 2 series |
| `pandas~=2.2.0` | 2.2.x but not 2.3 ("compatible release") |

**Trap:** in a terminal the `>` sign means "write the output to a file".
Type `python -m pip install pandas>=2.0` and pip installs `pandas` while its
output goes into a file called `=2.0`. Put any version with a comparison sign
**in quotes**:

```text
python -m pip install "pandas>=2.0"
```

## What is an environment?

The moment you install Python you have an environment: that Python and its
`site-packages` folder. This is called the **global** environment. Unless you
do something else, every `pip install` lands there.

For one project that is fine. The trouble starts with the second.

<figure class="fig">
  <div class="flow">
    <span class="node no"><b>Project A</b><br>wants pandas 1.5</span>
    <span class="arrow">→</span>
    <span class="node"><b>Global environment</b><br>one pandas version</span>
    <span class="arrow">←</span>
    <span class="node no"><b>Project B</b><br>wants pandas 2.2</span>
  </div>
  <figcaption>An environment can hold only one version of a package. Upgrade pandas for B and A breaks.</figcaption>
</figure>

Using the global environment costs you three things:

- **Conflicts.** An environment holds only one version of each package.
- **"It works on my machine."** You do not know which packages the project
  really needs; nobody can tell which of the hundred packages collected in
  the global environment over the years you actually use.
- **Cleanliness.** When you drop a project you cannot pick out the packages
  you installed for it.

The fix is to give **every project its own environment**.

## Virtual environments: `venv`

A virtual environment is a small folder inside the project folder. It holds
a Python command for that project and an **empty** `site-packages`.
Everything you install in it goes there; the global environment and other
projects are untouched.

`venv` ships with Python; you do not install it separately.

### Creating one

In the project folder:

```text
python -m venv .venv
```

The last word is the environment's folder name. `.venv` is a convention: VS
Code finds it on its own and the leading dot marks it as hidden. What you
get (Windows):

```text
project-a/
├── .venv/
│   ├── pyvenv.cfg          which Python created it
│   ├── Scripts/            python.exe, pip.exe, activate
│   └── Lib/
│       └── site-packages/  this project's packages
└── main.py
```

On macOS and Linux it is `bin` instead of `Scripts`, and the packages live
under `lib/python3.x/site-packages`.

`venv` does not copy Python from scratch; it writes the location of the
Python that created it into `pyvenv.cfg`. So **the environment's Python
version is the version of the Python that created it.** If you want another
version, create the environment with that version:

```text
py -3.11 -m venv .venv
```

### Activating it

| Terminal | Command |
|---|---|
| Windows `cmd` | `.venv\Scripts\activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

When it works, the environment's name appears at the start of the prompt:

```text
(.venv) C:\projects\project-a>
```

From now on `python` and `python -m pip` are this environment's. To leave:

```text
deactivate
```

### What does activating actually do?

No magic. `activate` puts the environment's `Scripts` folder at the **very
front** of `PATH`. When Windows looks for `python` it finds that one first.
To check:

```text
where python
```

The first line should be `...\project-a\.venv\Scripts\python.exe`.

Knowing this helps, because activating is **not required**. You can call the
environment's Python by its path:

```text
.venv\Scripts\python main.py
.venv\Scripts\python -m pip install pandas
```

### New terminal, activate again

Activation applies only to **that terminal window**. Close it and open a new
one and the environment is off again. First thing in a new window:
`activate`.

### Deleting and moving

To delete an environment, delete its folder. There is no uninstaller and
nothing registered anywhere.

**Do not move or rename** the environment folder. Full paths are written
into the scripts inside; a moved environment breaks. If you moved the
project folder, delete `.venv` and create it again. That is why we keep the
project's package list in a file.

## Two environments side by side

Two projects, two different pandas versions, one computer:

```text
cd C:\projects\project-a
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas==1.5.3
python -c "import pandas; print(pandas.__version__)"
1.5.3
deactivate

cd C:\projects\project-b
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas==2.2.2
python -c "import pandas; print(pandas.__version__)"
2.2.2
```

Each project sees its own version and knows nothing of the other. The global
environment has no pandas at all.

**What connects you to an environment is which Python is running at that
moment.** In the terminal, `activate` decides that. Your editor has to be
told separately: "Python: Select Interpreter" in VS Code, the kernel choice
in Jupyter. How to do both is in the "Connecting Your Editor" note.

To ask from inside your code which Python you are in:

```python
import sys
print(sys.executable)
```

That is the first thing to check when you get `ModuleNotFoundError`.

## `requirements.txt`

You never share the environment itself: it is large, specific to your
computer and does not work anywhere else. What you share is the **recipe**:
which packages, in which versions. By convention that recipe is called
`requirements.txt`.

```text
# Project A's packages
pandas==2.2.2
numpy==1.26.4
matplotlib>=3.8
```

One package per line. A line starting with `#` is a comment.

Writing the environment's packages to the file:

```text
python -m pip freeze > requirements.txt
```

That `>` is the same "write the output to a file" sign. `freeze` writes every
package with its exact version, **dependencies included**: install pandas
and the file also lists NumPy, python-dateutil and pytz. This lets the
project be rebuilt exactly the same elsewhere. You can also write the file by
hand; then you list only the packages you use directly.

Installing everything in the file:

```text
python -m pip install -r requirements.txt
```

**Do not run `freeze` in the global environment.** Everything collected
there over the years ends up in the file. `freeze` only makes sense in the
project's own environment.

### Sharing with Git

The `.venv` folder does not go into the repository; `requirements.txt` does.
Add this line to the project's `.gitignore`:

```text
.venv/
```

When you get someone else's project the steps are always the same:

```text
git clone https://github.com/someone/project.git
cd project
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Anaconda and conda

Data science resources often recommend **Anaconda**. Anaconda is a
**distribution**: one installer brings Python, a manager called `conda`,
hundreds of ready-made data science packages, Jupyter and a graphical tool
called Anaconda Navigator.

The same family has two smaller siblings:

- **Miniconda:** only Python and conda. You install the packages yourself.
- **Miniforge:** small like Miniconda; takes packages from the community's
  `conda-forge` channel.

### What does conda do differently?

`conda` is both a package manager and an environment manager. It differs
from pip in three important ways:

1. **It installs more than Python packages.** C and C++ libraries, graphics
   card tools (CUDA), even other languages such as R can be conda packages.
   If a Python package depends on such a system library, conda brings that
   too.
2. **It installs Python itself.** `venv` uses whichever Python created it;
   conda downloads the version you ask for into the environment.
3. **Environments live in one central place, not in the project folder.** You
   refer to them by name; their files sit under `anaconda3\envs\<name>`.

### Environments with conda

```text
conda create -n project-a python=3.11
conda activate project-a
conda install pandas
conda deactivate
```

`-n` is the environment's name. The active environment again appears at the
start of the prompt: `(project-a)`.

Installing conda also gives you a **`base`** environment, and it becomes
active whenever a terminal opens. **Do not install project packages into
`base`.** That is conda's own working space; break it and conda breaks. Open
a new environment for each project with `conda create`.

On Windows conda works most easily in the **Anaconda Prompt** window. If
`conda activate` fails in a normal PowerShell, run this once and reopen the
terminal:

```text
conda init powershell
```

### The environment file: `environment.yml`

conda's counterpart of `requirements.txt`. It records the Python version as
well:

```text
name: project-a
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pandas=2.2
  - pip
  - pip:
      - some-pypi-package==1.0
```

```text
conda env export > environment.yml
conda env create -f environment.yml
```

Here the version takes a single `=` (`pandas=2.2`); in pip it was `==`. One
of the details people mix up most.

### Channels and licensing

conda packages come from **channels**. Anaconda's own channel is `defaults`;
the community's is `conda-forge`. To install from a particular channel:
`conda install -c conda-forge package`.

Anaconda's own channel and distribution require a commercial licence in
larger organisations. If you will use it at a company, check the company's
rules first. Miniforge and `conda-forge` are not subject to that condition.

## pip or conda?

<figure class="fig">
  <div class="versus">
    <div>
      <h5>PIP + VENV</h5>
<pre><code class="language-text">python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas</code></pre>
    </div>
    <div>
      <h5>CONDA</h5>
<pre><code class="language-text">conda create -n demo python=3.11
conda activate demo
conda install pandas</code></pre>
    </div>
  </div>
  <figcaption>The same job with two tools: create an environment, activate it, install a package. Both solve the same problem; they differ in what they can install and where they keep the environment.</figcaption>
</figure>

| | pip + venv | conda |
|---|---|---|
| Comes from | Python itself | Anaconda / Miniconda / Miniforge |
| Package source | PyPI | `defaults`, `conda-forge` channels |
| What it installs | Python packages | Python packages **and** non-Python libraries |
| Python version | That of the Python that created it | Chosen as `python=3.11`, conda downloads it |
| Where environments live | In the project folder (`.venv`) | Centrally (`envs\<name>`) |
| Activating | `.venv\Scripts\activate` | `conda activate <name>` |
| Recipe file | `requirements.txt` | `environment.yml` |

### Using both together

pip works inside a conda environment too; you may need it for a package
conda does not have. The rule:

1. Install everything you can with **conda** first.
2. Install whatever conda does not have with **pip**, last.
3. After pip, do not go back to `conda install` in the same environment.
   conda does not fully know what pip installed and may overwrite it.

If things get tangled, do not try to repair the environment; delete it and
rebuild it from the file. That is what environments being cheap means.

One more thing: if the prompt shows **two environments at once**, like
`(.venv) (base)`, one of them is too many. Close one first with
`deactivate` / `conda deactivate`.

## Which one to start with?

**A clean Python from python.org, `venv` for every project, and `pip`.**
That is the standard; most projects in job listings, open source
repositories and documentation are set up this way. Everything you learn
here still helps when you move to conda.

Choose conda when:

- You quickly need a Python version you do not have.
- You need libraries that use the graphics card, or non-Python system
  libraries.
- Your team or course uses conda.

## Starting a project

The same five steps for every new project:

```text
mkdir project-a
cd project-a
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas
```

Whenever the packages change:

```text
python -m pip freeze > requirements.txt
```

## Summary

- The **interpreter** is the program that runs code; an **environment** is
  that interpreter plus the packages installed for it.
- A package is installed into the Python that installed it. So write
  **`python -m pip`**, not `pip`.
- In a terminal, versions with comparison signs go in quotes:
  `"pandas>=2.0"`.
- **One environment per project.** `python -m venv .venv` creates it,
  `.venv\Scripts\activate` activates it, `deactivate` closes it.
- Activating puts the environment at the front of `PATH` and applies only to
  that terminal window.
- You share the recipe, not the environment: `requirements.txt`
  (`pip freeze >` writes it, `pip install -r` installs it). `.venv/` goes in
  `.gitignore`.
- **Anaconda** is a distribution, **conda** a package and environment
  manager. It can install non-Python libraries and Python itself, and keeps
  environments centrally. Do not install into `base`.
- In a conda environment, conda first and pip last.
- When you get `ModuleNotFoundError`, the first question is: **which Python
  is running?**
