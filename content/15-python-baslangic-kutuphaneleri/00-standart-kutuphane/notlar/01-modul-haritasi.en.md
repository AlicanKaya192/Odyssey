Which standard library module do you look at for a given job? What this module
teaches, and what should come to mind first:

| Job | Module | Section |
|---|---|---|
| Square root, logarithm, combinations | `math` | math and statistics |
| Mean, median, standard deviation | `statistics` | math and statistics |
| Random numbers, shuffling, sampling | `random` | random |
| Dates, times, time differences | `datetime` | datetime |
| Measuring time, waiting | `time` | time and Measuring Time |
| Environment variables, command-line arguments | `os`, `sys` | os and sys |
| File paths, walking folders | `pathlib` | pathlib |
| Copying, moving, finding files by pattern | `shutil`, `glob` | shutil and glob |
| Reading/writing table files | `csv` | csv |
| JSON | `json` | Python path, JSON section |
| Searching patterns in text | `re` | Regular Expressions |
| Counters, queues, default dictionaries | `collections` | collections |
| Combinations, grouping, chaining | `itertools` | itertools |
| Wrapping text, Unicode | `textwrap`, `string`, `unicodedata` | Text Tools |
| zip, gzip, temporary files | `zipfile`, `gzip`, `tempfile` | Archives and Temporary Files |
| Copies, pretty printing, constant names | `copy`, `pprint`, `enum` | copy, pprint and enum |

In the advanced Python module: `functools`, `typing`, `dataclasses`,
`contextlib`, `logging`, `argparse`, `sqlite3`, `pickle`, `decimal`,
`hashlib`, `concurrent.futures`, `asyncio`, `unittest`, `timeit`.

## Reading the documentation

- In the interactive shell, `help(module)` or `help(module.function)`.
- The official documentation: docs.python.org → Library Reference; every
  module's page has examples.
- The documentation says "Added in version 3.x" for a function; if it is
  missing in an older Python, that is why.
