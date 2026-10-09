This module showed the **everyday** side of the standard library: numbers,
dates, files, text, data structures. Growing projects bring other needs, and
most of those are in the standard library too.

## Python Libraries: Advanced

The next module covers the tools of bigger programs:

- **Working with functions:** `functools` (`lru_cache`, `partial`),
  `operator`, sort keys.
- **Writing clear code:** type hints with `typing`, record classes with
  `dataclasses`, `abc` and protocols.
- **Managing resources:** writing your own `with` blocks with `contextlib`.
- **Real programs:** `logging` (records instead of print), `argparse` (a
  command line tool), `sqlite3` (a database in a file), `pickle` and
  serialisation.
- **Exact arithmetic and security:** `decimal` (money), `fractions`,
  `hashlib` (digests), `secrets` (secure randomness).
- **Speed:** `threading`, `concurrent.futures`, `asyncio`; measuring with
  `timeit` and `cProfile`.
- **Robust code:** `unittest`, `doctest`; memory leaks and how to prevent
  them.

## The data science side

The third and fourth modules of this path go beyond the standard library:
NumPy, pandas, Matplotlib, seaborn, SciPy, then scikit-learn and model
libraries. What you learned here holds there too: pandas formats dates like
`datetime`, uses regex on columns with `.str`, and takes file paths as
`Path`.

## Exploring on your own

- All functions of a module: `dir(module)`, a description: `help(module.name)`.
- Python's official documentation has a "The Python Standard Library" page
  listing the modules by topic; every module page has examples.
- For any job, first ask "is it in the standard library?": if so, no
  installation, no version problems, the same on every computer.
