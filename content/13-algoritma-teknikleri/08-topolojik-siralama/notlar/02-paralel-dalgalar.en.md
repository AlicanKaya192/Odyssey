Jobs that do not wait for each other can run at the same time.
`graphlib.TopologicalSorter` supports this directly: `get_ready()` gives
**all** the jobs that can start right now, `done()` reports the finished ones.

```python
from graphlib import TopologicalSorter

deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}

sorter = TopologicalSorter(deps)
sorter.prepare()
wave = 1
while sorter.is_active():
    ready = sorted(sorter.get_ready())     # all of them can run at once now
    print("wave", wave, ready)
    sorter.done(*ready)                    # in reality: as the jobs finish
    wave += 1
```

```text
wave 1 ['extract']
wave 2 ['clean', 'validate']
wave 3 ['features']
wave 4 ['train']
wave 5 ['evaluate']
wave 6 ['report']
```

In the second wave `clean` and `validate` can run at the same time. In a real
pipeline jobs finish at different times; `done()` is called whenever a job
finishes and `get_ready()` gives the newly opened jobs. Combined with
`concurrent.futures` it becomes a small job scheduler; the core of Airflow is
this idea too.
