# What Is Big Data?

In the Data Science track everything went the same way: read the file with
`pd.read_csv`, work with the table. As long as the file is a few megabytes,
that road is flawless. But what if the file is 50 gigabytes?

Most of the time the program **crashes** or the computer freezes for
minutes. There is nothing wrong with the code; the problem is that the data
**does not fit in the computer's memory**.

This track is about exactly that moment: what do you do when the data is
bigger than your tools can comfortably carry? In this first section we learn
no new tool. First we understand the problem itself: what is memory, how much
room does a table take there, and what does "big" actually mean?

## Big for whom?

Big data has no fixed threshold. There is no rule like "anything over a
million rows is big". The useful definition is this:

> Data is big when it is **more than the machine and the tool you want to
> process it with can comfortably carry**.

The same 20 GB file is big for a laptop with 8 GB of memory and ordinary for
a server with 256 GB. The same file can be hard for pandas and easy for a
database. So the question is always: does **this data, on this machine, with
this tool** cause trouble?

That is why you will not learn a single "big data tool" on this track. You
will learn a toolbox: shrinking the data, processing it piece by piece,
switching to a better file format, taking the work to the data, and splitting
the work across several cores or machines.

## Memory and disk

Data on your computer can live in two separate places:

- **Disk** (SSD or hard disk): where files live. Large and permanent; the data
  is still there when the computer is off. Today's laptops usually have
  512 GB or 1 TB.
- **Memory** (RAM): where a program works **right now**. Small and temporary;
  it empties when the program closes. Usually 8, 16 or 32 GB.

An analogy: the disk is the shelves of a library, memory is your desk. To
read a book you have to take it off the shelf and put it on the desk. The desk
is much smaller than the shelves but within reach; looking at a page on the
desk is many times faster than walking to the shelf each time.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Memory (RAM)</h4><p>The desk<br>Usually 8–32 GB<br>Very fast<br>Empties when the program closes</p></div>
    <div><h4>Disk (SSD)</h4><p>The library shelves<br>Usually 512 GB – 1 TB<br>Slower than memory<br>Permanent</p></div>
  </div>
  <figcaption>To work, pandas moves the table from disk into memory. The desk is much smaller than the shelves: a big data problem is usually a "does not fit on the desk" problem.</figcaption>
</figure>

When you write `pd.read_csv("orders.csv")`, pandas reads the **whole** file
from disk and puts it in memory. If the table fits on the desk, fine. If it
does not, one of two things happens:

1. Python cannot allocate memory and raises a `MemoryError`.
2. Windows tries to make room by moving part of memory to disk (this is
   called the *page file*). The program does not crash, but since the disk is
   much slower than memory, the computer starts to crawl.

In Odyssey an exercise can use at most **3 GB** of memory; if your code goes
over that, the run is stopped and the terminal says so. The exercises on this
track stay far below that limit, but the limit is a good reminder: memory is
not infinite.

## Bytes, kilobytes, megabytes

Everything in memory and on disk is measured in **bytes**. A byte is the
smallest unit, able to hold a number from 0 to 255. Larger units grow by
factors of 1024:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>1 byte</span><span>a number from 0 to 255</span></div>
    <div class="anat-row"><span>1 KB</span><span>1024 bytes: a short text</span></div>
    <div class="anat-row"><span>1 MB</span><span>1024 KB: a photo, a table of thousands of rows</span></div>
    <div class="anat-row"><span>1 GB</span><span>1024 MB: a film, tens of millions of rows</span></div>
    <div class="anat-row"><span>1 TB</span><span>1024 GB: a company's records piled up over years</span></div>
  </div>
  <figcaption>Each step is 1024 times the previous one: from bytes to gigabytes is three steps, 1024 × 1024 × 1024.</figcaption>
</figure>

Why 1024 and not 1000? Computers work in binary, and 1024 is 2 to the power
of 10. On this track we do what Windows does and count 1 MB as 1024 × 1024
bytes. In code that is written `1024**2`:

```python
size_in_bytes = 5_000_000
print(size_in_bytes / 1024**2, "MB")
```

```text
4.76837158203125 MB
```

> Disk makers, on the other hand, count 1 GB as 1 000 000 000 bytes. That is
> why a disk sold as "1 TB" shows up as 931 GB in Windows: both say the same
> amount in different units.

## How much room does a number take?

pandas and NumPy store numbers at a fixed width. The two types you see most:

- `int64`: a whole number, **8 bytes**
- `float64`: a decimal number, **8 bytes**

This means you can work out on paper how much room a table will take. A table
with 10 million rows and 6 numeric columns:

```python
rows = 10_000_000
columns = 6
size = rows * columns * 8
print(size / 1024**2, "MB")
print(round(size / 1024**3, 2), "GB")
```

```text
457.763671875 MB
0.45 GB
```

Half a gigabyte. No problem for a computer with 16 GB of memory. But if the
same table had a billion rows it would pass 45 GB.

## A Python list versus a NumPy array

Let us store the same million numbers in two different ways and measure:

```python
import sys
import numpy as np

numbers = list(range(1_000_000))
array = np.arange(1_000_000)

list_mb = (sys.getsizeof(numbers) + sum(sys.getsizeof(x) for x in numbers)) / 1024**2
array_mb = array.nbytes / 1024**2
print(f"list:  {list_mb:.1f} MB")
print(f"array: {array_mb:.1f} MB")
```

```text
list:  34.3 MB
array: 7.6 MB
```

The list takes **four and a half times** the room. Here is why: in a Python
list every number is a separate object. Each object has its own header
(information such as its type and how many places use it), and the list only
holds the **addresses** of those objects. A NumPy array lines the numbers up
side by side, with no headers: each number exactly 8 bytes.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Python list</h4><p>The list only holds addresses: 8 bytes per number<br>Every number is a separate object: 28 bytes<br><b>About 36 bytes per number</b></p></div>
    <div class="ok"><h4>NumPy array</h4><p>Numbers side by side, no headers<br><code>int64</code>: 8 bytes<br><b>8 bytes per number</b></p></div>
  </div>
  <figcaption>For a million numbers, 34.3 MB against 7.6 MB. pandas stores columns much like NumPy arrays.</figcaption>
</figure>

`sys.getsizeof(x)` gives an object's size in bytes. The list's own size
includes only the addresses; we added up the numbers inside it separately.
This is one reason pandas is so much better than Python lists for big data: it
stores columns tightly, like NumPy arrays.

## File size does not tell you the size in memory

The data we will use often on this track is a shop's orders from 2024. Next
to the exercises there will be a read-only `orders_data.py` file; its
`make_orders(n)` produces the **same** `n` rows every time. That way nobody
has to download big files: everyone produces the same table on their own
computer.

```python
import pandas as pd
from orders_data import make_orders

df = make_orders(5)
print(df.iloc[:, :4].to_string(index=False))
print()
print(df.iloc[:, 4:].to_string(index=False))
```

```text
 order_id          order_time  customer_id    city
        1 2024-04-11 21:41:26            3   Izmir
        2 2024-04-20 21:50:12            9 Trabzon
        3 2024-05-05 00:38:40            5 Antalya
        4 2024-09-20 07:49:57            5   Izmir
        5 2024-10-25 19:49:47            5 Trabzon

   category  quantity  unit_price  payment
       toys         2      226.16     card
   clothing         1      531.06     card
   clothing         4      831.23     card
electronics         1     2020.20     card
electronics         4     1931.51 transfer
```

The table is wide, so we printed it in two parts: the first four columns, then the last four.

Now let us write a million orders to a CSV file, read it back and compare the
two sizes:

```python
import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
df = pd.read_csv("orders.csv")

file_mb = os.path.getsize("orders.csv") / 1024**2
memory_mb = df.memory_usage(deep=True).sum() / 1024**2
print(f"rows:   {len(df):,}")
print(f"file:   {file_mb:.1f} MB")
print(f"memory: {memory_mb:.1f} MB")
```

```text
rows:   1,000,000
file:   61.1 MB
memory: 95.9 MB
```

There are two new tools:

- `os.path.getsize(path)`: the size of the file on disk, in bytes.
- `df.memory_usage(deep=True)`: how many bytes each column takes in memory;
  with `.sum()`, the whole table. `deep=True` makes it look inside the text
  columns too (more on this in the next section).

The 61 MB file became 96 MB in memory. The file size does **not** tell you
how much the data will take in memory; you have to measure.

### The same table, two ways of storing it

Older versions of pandas stored text as a separate Python object in every cell
(the `object` type). pandas 3, which you are using, stores text in a much
tighter form (the `str` type). Let us read the same file both ways:

```python
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
text_columns = ["order_time", "city", "category", "payment"]
old = pd.read_csv("orders.csv", dtype={c: object for c in text_columns})
new = pd.read_csv("orders.csv")
print(f"object: {old.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
print(f"str:    {new.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
```

```text
object: 252.3 MB
str:    95.9 MB
```

The same data, the same rows: one is 252 MB, the other 96 MB. The rule you
will often read online, "pandas needs 5 to 10 times the file size in memory",
comes from the old `object` storage. Instead of a rule, make **measuring** a
habit: the pandas version, the column types and the length of the text all
change the result.

## The three Vs of big data

Three words come up again and again when big data is explained. In English
they all start with V:

- **Volume:** how big the data is. The main subject of this track.
- **Velocity:** how fast the data arrives. Thousands of clicks a second on a
  website, sensors in a factory sending a reading every second. The data is
  not a finished file but a flowing river (Section 14).
- **Variety:** the shape of the data. Tables, JSON records, text, images,
  sound, all together.

Some sources add two more Vs: **Veracity** (how trustworthy is the data?) and
**Value** (does anything useful come out of it?). If an exam asks you to
"define big data", listing the three Vs with examples is a good start.

## Two ways to grow: vertical and horizontal

When the data does not fit the machine there are two options:

<figure class="fig">
  <div class="versus">
    <div><h4>Scaling up</h4><p>A <b>single</b>, more powerful machine<br>The code does not change<br>It has a limit; the price rises fast</p></div>
    <div><h4>Scaling out</h4><p><b>More</b> machines<br>The work is split, the results combined<br>Almost no limit; hard to set up</p></div>
  </div>
  <figcaption>Also called vertical and horizontal scaling. Spark and Hadoop exist for scaling out.</figcaption>
</figure>

- **Scaling up** (vertical): a more powerful machine. 256 GB of memory
  instead of 16. Your code does not change at all, but there is a limit: you
  cannot buy bigger than the biggest machine in the world, and the price rises
  fast.
- **Scaling out** (horizontal): more machines. Split the data into pieces and
  give each piece to a different machine. There is almost no limit, but you
  have to split the work, combine the results and cope with a machine that
  breaks. Hadoop and Spark exist for this (Sections 12 and 13).

Often the best first step is neither: **working smarter on the same
machine**. The three columns you need from a 100 GB file may take 5 GB. The
first half of the track is about this.

## The map of this track

<figure class="fig">
  <div class="flow">
    <span class="node">Measure</span><span class="arrow">→</span>
    <span class="node">Shrink</span><span class="arrow">→</span>
    <span class="node">Split</span><span class="arrow">→</span>
    <span class="node">Right format</span><span class="arrow">→</span>
    <span class="node acc">Distribute</span>
  </div>
  <figcaption>The order of the track is also the order to try things in when you hit a problem: the cheap and simple first, several machines last.</figcaption>
</figure>

1. **Measure** (Section 1): how much does the table take in memory, which
   column is the most expensive?
2. **Shrink** (Section 2): with the right data types the same table takes
   less room.
3. **Split** (Section 3): read the file piece by piece, not all at once.
4. **The right format** (Sections 4–6): Parquet instead of CSV; read only the
   columns and rows you need.
5. **Take the work to the data** (Sections 7–8): SQL straight on top of the
   file with DuckDB.
6. **Make do with less data** (Section 9): sampling and approximation.
7. **Divide and distribute** (Sections 10–14): cores, dask, MapReduce, Spark
   and streaming data.

## Measure first, then fix

The most important habit on this track: **do not guess, measure.** If you
think something is slow or big, get the number first:

- How big is the file? `os.path.getsize`
- How big is the table in memory? `df.memory_usage(deep=True).sum()`
- Which column takes the most room? `df.memory_usage(deep=True)` (Section 1)

An improvement made without measuring usually lands in the wrong place.

## Summary

- Data is **big** when it is too much for the machine and tool that process
  it; there is no fixed threshold.
- The **disk** is large and permanent, **memory** small and fast. pandas
  reads a file into memory from start to end.
- 1 KB = 1024 bytes, 1 MB = 1024² bytes. `int64` and `float64` take 8 bytes
  per number.
- A Python list stores every number as a separate object; a NumPy array
  stores them side by side. For a million numbers, 34.3 MB against 7.6 MB.
- File size does not tell you the size in memory: a 61 MB CSV is 96 MB in
  pandas 3 and 252 MB with the old `object` storage.
- Three Vs: volume, velocity, variety.
- Scaling up is a bigger machine, scaling out is more machines. First try
  working smarter on the same machine.
