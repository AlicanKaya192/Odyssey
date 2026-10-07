# MapReduce

Everything so far happened on **a single computer**: smarter types, chunked
reading, cores. But what if the data is hundreds of terabytes and does not fit
even on the disk of any single machine? Scaling out from Section 0: **many
machines**.

The hard part of working with many machines is not the machines themselves
but splitting the work between them: which machine processes which data, how
the results are combined, what happens if a machine breaks? In 2004 Google
published a simple answer to these questions: **MapReduce**. The programmer
writes only two small functions; the system handles the rest. Hadoop became
the open source implementation of this idea that everyone could use, and it
made the words "big data" spread.

In this section we build MapReduce ourselves, step by step, in pure Python.
The aim is not to set up a cluster; it is to understand the thinking behind
every tool that runs on a cluster (Hadoop, Spark, dask).

## Storage first: HDFS

Hadoop's file system **HDFS** splits a big file into **blocks** (128 MB by
default) and writes each block to different machines in **three copies**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Block 1 (128 MB)</span><span>Machine A · Machine C · Machine E</span></div>
    <div class="anat-row"><span>Block 2 (128 MB)</span><span>Machine B · Machine D · Machine A</span></div>
    <div class="anat-row"><span>Block 3 (128 MB)</span><span>Machine C · Machine E · Machine B</span></div>
    <div class="anat-row"><span>…</span><span>each block on three separate machines</span></div>
  </div>
  <figcaption>In HDFS a big file is split into blocks and copied. Even if one machine breaks, two copies of every block remain.</figcaption>
</figure>

Two things follow from this:

1. **A broken machine is not a disaster.** Even if one copy of a block is
   lost, two copies sit on other machines.
2. **Take the code to the data.** Moving 1 TB of data over the network to a
   single machine takes hours; sending a program of a few kilobytes to the
   machines where the data lives takes seconds. MapReduce processes each piece
   on the machine where that piece is stored.

## Three steps: map, shuffle, reduce

<figure class="fig">
  <div class="flow">
    <span class="node">Blocks</span><span class="arrow">→</span>
    <span class="node">Map<br>(key, value)</span><span class="arrow">→</span>
    <span class="node">Shuffle<br>group</span><span class="arrow">→</span>
    <span class="node">Reduce<br>combine</span><span class="arrow">→</span>
    <span class="node acc">Result</span>
  </div>
  <figcaption>The programmer writes map and reduce; the system handles the shuffle, the spreading and the broken machine.</figcaption>
</figure>

1. **Map:** for each record, produce one or more **(key, value)** pairs. Each
   machine does this for the records in its own block.
2. **Shuffle:** gather all the pairs with the same key **in the same place**,
   whichever machine they come from.
3. **Reduce:** produce a single result from each key's list of values.

The programmer writes only the `map` and `reduce` functions. The system does
the shuffle, the spreading over machines and the broken machine.

## The classic example: counting words

How many times each word appears in a three-line text:

```python
from collections import defaultdict

text = ["the cat sat", "the dog sat", "the cat ran"]

def mapper(line):
    for word in line.split():
        yield word, 1

pairs = [pair for line in text for pair in mapper(line)]
print(pairs[:4])
print(len(pairs))
```

```text
[('the', 1), ('cat', 1), ('sat', 1), ('the', 1)]
9
```

`mapper` takes a line and produces a `(word, 1)` pair for each word. `yield`
lets a function **produce** values one by one (this function is a
generator); there is no need to build a list and return it.

Shuffle: gather all the values of the same word in a list.

```python
groups = defaultdict(list)
for key, value in pairs:
    groups[key].append(value)
print(dict(groups))
```

```text
{'the': [1, 1, 1], 'cat': [1, 1], 'sat': [1, 1], 'dog': [1], 'ran': [1]}
```

`defaultdict(list)`: a dictionary that opens an empty list by itself the first
time a missing key is used.

Reduce: add up each word's list.

```python
def reducer(key, values):
    return key, sum(values)

print(sorted(reducer(k, v) for k, v in groups.items()))
```

```text
[('cat', 2), ('dog', 1), ('ran', 1), ('sat', 2), ('the', 3)]
```

Three steps on three lines. The same three functions can be applied to three
lines or to three billion; the only difference is how many machines are
working.

## MapReduce on the orders

Let us work out the revenue per city, which we have known since Section 3,
with MapReduce. Each order is a record:

```python
rows = orders[["city", "quantity", "unit_price"]].to_dict("records")

def mapper(row):
    yield row["city"], row["quantity"] * row["unit_price"]

def reducer(key, values):
    return key, sum(values)

groups = defaultdict(list)
for row in rows:
    for key, value in mapper(row):
        groups[key].append(value)
result = dict(reducer(k, v) for k, v in groups.items())
```

Istanbul 557.00, Ankara 260.83, Izmir 212.50 million: the same as the results
in Sections 3, 7 and 11.

On a single machine this way is slow: 0.49 seconds for a million orders,
against 0.058 seconds for pandas' `groupby`. MapReduce's value is not speed on
one machine; it is that the same code can be split across **hundreds of
machines**.

## The combiner: protecting the network

In the shuffle step the pairs travel between machines **over the network**,
and the network is the slowest part of a cluster. Suppose we split a million
orders over four machines. If each machine sends a pair for every order, a
million pairs cross the network.

But each machine can add up **its own pairs** per city before sending them.
This is called a **combiner**:

```python
chunks = [orders.iloc[i * 250_000:(i + 1) * 250_000] for i in range(4)]
without = 0
with_combiner = 0
for chunk in chunks:
    pairs = list(zip(chunk["city"], chunk["quantity"] * chunk["unit_price"]))
    without += len(pairs)
    local = defaultdict(float)
    for key, value in pairs:
        local[key] += value
    with_combiner += len(local)
print(without, with_combiner)
```

```text
1000000 32
```

32 pairs instead of a million (4 machines × 8 cities). The distributed form of
Section 3's "summarise in the piece, combine the summaries" pattern. And the
same limit applies: totals and counts work with a combiner, a median does not.

## Sending a key to a machine

To keep the "same key, same place" rule in the shuffle, each key needs a
**reduce machine**. The common way: take the key's **hash** and look at the
remainder when dividing by the number of machines.

Python's `hash()` function is the first tool that comes to mind, but it has a
trap. I ran the same line in five separate Python processes:

```python
print(hash("Istanbul") % 4)
```

```text
2
1
0
2
1
```

Five processes, five different answers. For security, Python works out the
hash of a string with a random seed in each process. If different machines
give different answers to "where does Istanbul go?", Istanbul's values are
scattered and the result breaks. The fix is a **stable** hash that gives the
same result everywhere: `zlib.crc32`.

```python
import zlib

def partition(key, reducers):
    return zlib.crc32(key.encode()) % reducers
```

`partition("Istanbul", 4)` is 1 in every process, on every machine.

## Data skew

Spreading the eight cities over three reduce machines with
`partition(city, 3)`:

| Machine | Cities | Share of orders |
|---|---|---|
| 0 | Ankara, Antalya, Istanbul, Konya | 66% |
| 1 | Adana, Bursa, Izmir | 29% |
| 2 | Trabzon | 5% |

Machine 0 gets two thirds of the work; machine 2 finishes quickly and waits.
The whole job finishes only when **the slowest machine** finishes. This is
called **data skew**, and it is one of the most common causes of slowness on
real clusters.

Remedies:

- **More reduce machines:** the big key still stays on one machine, but the
  others spread out.
- **Salting the key:** splitting a very big key into pieces, for example
  `Istanbul#0`, `Istanbul#1`, `Istanbul#2`, and combining the piece results in
  a small second step.

## Grouping by sorting

Real MapReduce systems **sort the pairs by key** in the shuffle; the reduce
step passes through the sorted list once from start to end, gathering each
key's values. The Python counterpart is `itertools.groupby`:

```python
from itertools import groupby

pairs = [("b", 1), ("a", 1), ("b", 1), ("c", 1), ("a", 1)]
pairs.sort()
for key, group in groupby(pairs, key=lambda kv: kv[0]):
    print(key, sum(v for _, v in group))
```

```text
a 2
b 2
c 1
```

`groupby` only joins identical keys that sit **side by side**; if the list is
not sorted, the same key comes back as several groups. Hence the `sort()`
first. A sorted list is processed as a stream without holding all the groups
in memory; for big data it needs less memory than collecting in a dictionary.

## A broken machine

Out of hundreds of machines, one will surely break. In MapReduce that is
easy: each map task reads only its own block and its result changes nothing
else. If a machine is lost, the manager reruns that task on a machine where
**another copy** of the block lives. Tasks having no side effects ("the same
input gives the same output every time") makes this possible.

## The limits of MapReduce

- The result of every step is written to **disk**. Solid for single-pass jobs,
  but jobs that go over the data again and again (machine learning
  algorithms, graph calculations) are very slow because they write to and read
  from disk on every round.
- Turning everything into map and reduce is tedious: jobs such as a join take
  several MapReduce steps.

These two limits gave birth to the subject of the next section: **Spark**,
which keeps intermediate results **in memory** and offers a SQL-like language.

## Summary

- When data does not fit on one machine, many machines; HDFS splits a file
  into 128 MB blocks and keeps three copies of each; the code goes to the
  machine where the data is.
- MapReduce: **map** (record → key-value pairs), **shuffle** (same key, same
  place), **reduce** (a key's values → one result).
- A combiner adds up on each machine first: 32 pairs instead of a million.
- To send keys to machines, a stable hash (`zlib.crc32`); Python's `hash()`
  differs in every process.
- Data skew: if one machine gets two thirds of the work, everyone waits for
  it.
- Since every step writes to disk, it is slow for repeated work; that is why
  Spark was born.
