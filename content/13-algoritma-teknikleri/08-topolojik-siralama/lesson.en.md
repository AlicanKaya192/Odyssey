# Topological Sorting

In a data pipeline the order of the jobs matters: you cannot clean data before
extracting it, you cannot train a model before building the features. Rules
like "`clean` must come after `extract`" form a **directed** graph: an arrow
says "this first, then that". **Topological sorting** finds an order of jobs
in which every arrow points forward.

<figure class="fig">
<svg viewBox="0 0 770 260" width="770" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dim" d="M0 0L10 5L0 10z"/></marker></defs>
<line class="line" x1="79.5" y1="113.1" x2="158.7" y2="67.9" marker-end="url(#arr)"/>
<line class="line" x1="79.5" y1="146.9" x2="158.7" y2="192.1" marker-end="url(#arr)"/>
<line class="line" x1="219.5" y1="66.9" x2="298.7" y2="112.1" marker-end="url(#arr)"/>
<line class="line" x1="219.5" y1="193.1" x2="298.7" y2="147.9" marker-end="url(#arr)"/>
<line class="line" x1="364.0" y1="130.0" x2="424.0" y2="130.0" marker-end="url(#arr)"/>
<line class="line" x1="494.0" y1="130.0" x2="554.0" y2="130.0" marker-end="url(#arr)"/>
<line class="line" x1="619.0" y1="112.2" x2="689.3" y2="68.9" marker-end="url(#arr)"/>
<line class="line" x1="224.0" y1="50.0" x2="684.0" y2="50.0" marker-end="url(#arr)"/>
<circle class="box" cx="50" cy="130" r="34"/>
<text class="ink" x="50" y="133.8" font-size="11" text-anchor="middle">extract</text>
<circle class="box" cx="190" cy="50" r="34"/>
<text class="ink" x="190" y="53.9" font-size="11" text-anchor="middle">clean</text>
<circle class="box" cx="190" cy="210" r="34"/>
<text class="ink" x="190" y="213.8" font-size="11" text-anchor="middle">validate</text>
<circle class="box" cx="330" cy="130" r="34"/>
<text class="ink" x="330" y="133.8" font-size="11" text-anchor="middle">features</text>
<circle class="box" cx="460" cy="130" r="34"/>
<text class="ink" x="460" y="133.8" font-size="11" text-anchor="middle">train</text>
<circle class="box" cx="590" cy="130" r="34"/>
<text class="ink" x="590" y="133.8" font-size="11" text-anchor="middle">evaluate</text>
<circle class="box" cx="720" cy="50" r="34"/>
<text class="ink" x="720" y="53.9" font-size="11" text-anchor="middle">report</text>
</svg>
<figcaption>A data pipeline: each arrow says "this first, then that". There is no directed cycle; this is a DAG.</figcaption>
</figure>

Such an order exists only if the graph has **no directed cycle**: `A` cannot
come before `B` while `B` comes before `A`. A directed graph without cycles is
called a **DAG (directed acyclic graph)**. Course prerequisites, build systems
(`make`), the calculation order of spreadsheet formulas and data pipeline tools
like Airflow are DAGs.

## Kahn's algorithm: first the ones waiting for nothing

Count how many jobs each job **waits for** (its in-degree). Do the jobs left
waiting for nothing; for each job done, decrease the counter of the jobs
behind it by one, and add the new jobs that reach zero to the order.

```python
import heapq

deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}

def kahn(deps):
    nodes = set(deps) | {d for needs in deps.values() for d in needs}
    after = {n: [] for n in nodes}
    waiting = {n: 0 for n in nodes}          # how many jobs it waits for
    for task, needs in deps.items():
        for need in needs:
            after[need].append(task)
            waiting[task] += 1
    ready = [n for n in nodes if waiting[n] == 0]
    heapq.heapify(ready)                     # alphabetical on ties
    order = []
    while ready:
        task = heapq.heappop(ready)
        order.append(task)
        for nxt in after[task]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                heapq.heappush(ready, nxt)
    return order if len(order) == len(nodes) else None   # incomplete: a cycle

print(kahn(deps))
cyclic = dict(deps, extract=["report"])     # report → extract: a cycle
print(kahn(cyclic))
```

```text
['extract', 'clean', 'validate', 'features', 'train', 'evaluate', 'report']
None
```

In the cyclic graph no job's waiting count ever reaches zero; the order stops
halfway, and that **diagnoses** the cycle itself. Each node and edge once:
`O(n + m)`. An ordinary queue works too instead of a heap; the heap is only
there to guarantee alphabetical order on ties.

## With DFS: finish the dependencies first

Before doing a job, finish all its dependencies (with recursion), then add the
job to the list. To catch a cycle each node has three states: never seen,
**on the stack right now** (`active`), done (`done`). Coming back to a node
that is on the stack means a cycle.

```python
def dfs_order(deps):
    nodes = sorted(set(deps) | {d for needs in deps.values() for d in needs})
    state, order = {}, []
    def visit(task):
        if state.get(task) == "done":
            return True
        if state.get(task) == "active":       # back on its own path: a cycle
            return False
        state[task] = "active"
        for need in sorted(deps.get(task, [])):
            if not visit(need):
                return False
        state[task] = "done"
        order.append(task)                    # the dependencies are finished
        return True
    for task in nodes:
        if not visit(task):
            return None
    return order

print(dfs_order(deps), dfs_order(cyclic))
```

```text
['extract', 'clean', 'validate', 'features', 'train', 'evaluate', 'report'] None
```

## The ready-made one: `graphlib`

Python's standard library has `graphlib.TopologicalSorter`; it also reports a
cycle with an error and shows the cycle itself:

```python
from graphlib import TopologicalSorter, CycleError

print(list(TopologicalSorter(deps).static_order()))
try:
    list(TopologicalSorter(cyclic).static_order())
except CycleError as error:
    print("cycle:", error.args[1])
```

```text
['extract', 'clean', 'validate', 'features', 'train', 'evaluate', 'report']
cycle: ['clean', 'features', 'train', 'evaluate', 'report', 'extract', 'clean']
```

## The critical path: when can the pipeline finish at the earliest?

If each job has a duration and jobs that do not wait for each other can run at
the same time, the pipeline's finish time is the total of **the longest
dependency chain**. One pass in topological order is enough: a job finishes at
its own duration + the latest finish of its dependencies.

```python
hours = {"extract": 2, "clean": 3, "validate": 1, "features": 4,
         "train": 6, "evaluate": 1, "report": 2}
finish = {}
for task in kahn(deps):
    finish[task] = hours[task] + max((finish[d] for d in deps.get(task, [])), default=0)
for task, t in finish.items():
    print(task, t)
print("pipeline done after", max(finish.values()), "hours")
```

```text
extract 2
clean 5
validate 3
features 9
train 15
evaluate 16
report 18
pipeline done after 18 hours
```

The total work is 19 hours, but since `validate` can run at the same time as
`clean`, the pipeline finishes in 18 hours. `extract → clean → features →
train → evaluate → report` is the **critical path**: a delay in any of them
delays the whole pipeline. The critical path method (CPM) of project
management is exactly this.

## Summary

- Topological sorting: an order where every arrow points forward; it exists
  only in a DAG.
- Kahn: take what waits for nothing, decrease the counters behind it; if it
  stays incomplete, a cycle.
- DFS: dependencies first; coming back to an `active` node is a cycle.
- `graphlib.TopologicalSorter`: the ready-made one, with `CycleError`.
- The critical path: finish times in topological order; the longest chain.
- All of it is `O(n + m)`.
