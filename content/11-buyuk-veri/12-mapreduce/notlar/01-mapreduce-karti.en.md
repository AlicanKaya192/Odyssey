A skeleton for building MapReduce in pure Python, and the terms of the Hadoop
world.

## Skeleton

```python
from collections import defaultdict

def mapper(record):
    yield key, value                     # one or many pairs

def reducer(key, values):
    return key, sum(values)              # one result from a key's values

groups = defaultdict(list)               # shuffle
for record in records:
    for key, value in mapper(record):
        groups[key].append(value)

result = dict(reducer(k, v) for k, v in groups.items())
```

## The combiner

Each machine (piece) adds up its own pairs before sending them:

```python
local = defaultdict(float)
for key, value in pairs:
    local[key] += value
# only the pairs in local go over the network
```

A million orders, 4 pieces: 32 pairs instead of 1 000 000.

## The partitioner

```python
import zlib

def partition(key, reducers):
    return zlib.crc32(key.encode()) % reducers
```

Do not use `hash()`: Python works out a string's hash with a different seed in
each process (`hash("Istanbul") % 4` gave 2, 1, 0, 2, 1 in five processes).

## Grouping by sorting

```python
from itertools import groupby

pairs.sort()
for key, group in groupby(pairs, key=lambda kv: kv[0]):
    total = sum(v for _, v in group)
```

`groupby` only joins identical keys that sit side by side; sort first.

## Hadoop terms

| Term | Meaning |
|---|---|
| **HDFS** | Hadoop's distributed file system |
| **Block** | A piece of a file; 128 MB by default |
| **Replication** | Each block on three machines by default |
| **NameNode** | The manager that knows which block is on which machine |
| **DataNode** | A machine that stores blocks |
| **YARN** | The layer that hands the cluster's processors and memory to jobs |
| **Hive** | SQL on top of MapReduce |
| **Data locality** | Running the code on the machine where the data is |
| **Data skew** | One machine getting a disproportionate share of the data |
