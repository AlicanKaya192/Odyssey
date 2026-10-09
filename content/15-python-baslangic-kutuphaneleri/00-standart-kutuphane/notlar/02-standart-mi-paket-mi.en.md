Should you do a job with the standard library or with a package installed via
`pip`? The short rule: **look at the standard library first**, and install a
package if it is not enough.

## The standard library's advantages

- No installation: the script runs on any computer that has Python.
- No version trouble: it is updated with Python and documented in one place.
- More than enough for small jobs: reading a CSV, counting the files in a
  folder or finding the days between two dates does not need pandas.

## A package's advantages

- Speed on large data: on a computation over a million rows NumPy and pandas
  are much faster than plain Python (we measured it in the Algorithms path).
- Ready-made capabilities: machine learning (scikit-learn), plotting
  (Matplotlib), `requests` for HTTP requests and so on.

## Before using a package

- Is it really needed? Adding a big package for one small function burdens
  everyone who installs the project.
- Is it maintained? Look at the date of the latest release and its
  documentation.
- Which version? Pin the version in `requirements.txt` (like
  `pandas==3.0.6`); the Packages and Environments section of the Python path
  explains this.

## Watch out for name clashes

Do not give your own file the name of a standard library module: if you write
a file called `random.py`, `import random` in the same folder imports your
file instead, and `random.randint` is "missing". The error message looks
strange; the cause is the file name.
