This page is every command you need to know by heart. After reading the
lesson, come back here and test yourself: can you say what each line does?

The examples use Windows syntax. Where macOS and Linux differ, the table says
so.

## The ten most important commands

You should be able to type these in your sleep:

```text
python --version
where python
python -m venv .venv
.venv\Scripts\activate
deactivate
python -m pip install pandas
python -m pip list
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
```

## Python and the terminal

| Command | What it does |
|---|---|
| `python --version` | The version of the Python that runs |
| `where python` | Which files are found when you type `python`; the first line runs (macOS/Linux: `which python`) |
| `py --list` | Every installed Python version on Windows |
| `py -3.12` | Runs a specific version |
| `python main.py` | Runs a file |
| `python -m name` | Runs a module as a program (`-m pip`, `-m venv`) |
| `python -c "code"` | Runs a single line of code |
| `cd folder` | Enters a folder; `cd ..` goes up one |
| `dir` | Lists the folder (macOS/Linux and PowerShell: `ls`) |
| `mkdir project` | Creates a folder |

## pip

| Command | What it does |
|---|---|
| `python -m pip --version` | pip's version **and which Python it belongs to** |
| `python -m pip install name` | Installs |
| `python -m pip install name1 name2 name3` | Installs several at once |
| `python -m pip install name==1.2.3` | Exact version |
| `python -m pip install "name>=1.2"` | At least this version (quotes required) |
| `python -m pip install --upgrade name` | Upgrades (short form `-U`) |
| `python -m pip install --upgrade pip` | Upgrades pip itself |
| `python -m pip uninstall name` | Removes (`-y` skips the confirmation) |
| `python -m pip list` | Installed packages |
| `python -m pip list --outdated` | Packages with a newer version out |
| `python -m pip show name` | Version, location, dependencies |
| `python -m pip freeze` | A `name==version` list |
| `python -m pip check` | Checks that installed packages fit together |

## Virtual environments (`venv`)

| Command | What it does |
|---|---|
| `python -m venv .venv` | Creates the environment |
| `py -3.11 -m venv .venv` | Creates it with a specific Python version |
| `.venv\Scripts\activate` | Activates (`cmd`) |
| `.venv\Scripts\Activate.ps1` | Activates (PowerShell) |
| `source .venv/bin/activate` | Activates (macOS/Linux) |
| `deactivate` | Leaves the environment |
| `.venv\Scripts\python main.py` | Runs with the environment's Python without activating |
| `rmdir /s .venv` | Deletes the environment (`cmd`; PowerShell: `Remove-Item -Recurse .venv`, macOS/Linux: `rm -rf .venv`) |

## `requirements.txt`

| Command | What it does |
|---|---|
| `python -m pip freeze > requirements.txt` | Writes the environment's packages to the file |
| `python -m pip install -r requirements.txt` | Installs everything in the file |
| `python -m pip install -r requirements.txt --upgrade` | Moves everything in the file to the newest allowed version |

Inside the file:

```text
pandas==2.2.2       # exact version
numpy>=1.26         # at least
matplotlib~=3.8.0   # 3.8.x
requests            # no version: the newest
```

## conda

| Command | What it does |
|---|---|
| `conda --version` | conda's version |
| `conda create -n name python=3.11` | Creates an environment |
| `conda create -n name python=3.11 pandas numpy` | Creates it together with packages |
| `conda activate name` | Activates |
| `conda deactivate` | Leaves |
| `conda env list` | Every environment; `*` marks the active one |
| `conda list` | Packages in the active environment |
| `conda install name` | Installs |
| `conda install -c conda-forge name` | Installs from the `conda-forge` channel |
| `conda install name=1.2` | A specific version (single `=`) |
| `conda update name` | Upgrades |
| `conda remove name` | Removes |
| `conda env remove -n name` | Deletes the whole environment |
| `conda env export > environment.yml` | Writes the environment to a file |
| `conda env export --from-history > environment.yml` | Writes only what you installed yourself; works on other operating systems too |
| `conda env create -f environment.yml` | Creates an environment from the file |
| `conda env update -f environment.yml --prune` | Updates the environment to match the file, removing extras |
| `conda init powershell` | Makes `conda activate` work in PowerShell (once) |
| `conda config --set auto_activate_base false` | Stops `base` from activating when a terminal opens |
| `conda clean --all` | Clears the downloaded package cache |

## Jupyter and environments

| Command | What it does |
|---|---|
| `python -m pip install ipykernel` | The package needed to connect an environment to Jupyter |
| `python -m ipykernel install --user --name project-a` | Registers the active environment as a kernel called "project-a" |
| `jupyter kernelspec list` | Registered kernels |
| `jupyter kernelspec uninstall project-a` | Removes a kernel registration |
| `%pip install name` | In a notebook cell: installs into **that kernel's** environment |

## Easily confused

| This | Not this |
|---|---|
| `python -m pip install` | `pip install` (may go to another Python) |
| `"pandas>=2.0"` | `pandas>=2.0` (the terminal reads `>` as a redirect to a file) |
| `pandas==2.2` in pip | `pandas=2.2` in conda |
| `requirements.txt` is shared | `.venv` is not |
| `%pip install` (Jupyter) | `!pip install` (may go to another Python) |
| `pip install scikit-learn`, then `import sklearn` in code | `pip install sklearn` (the install name and import name can differ) |
