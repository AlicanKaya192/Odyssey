Measuring is easy; measuring wrongly is easier still. Each of these traps
ends with an improvement made in the wrong place.

## 1. Forgetting `deep=True`

On an `object` column `memory_usage()` counts only the addresses. For the
`city` column in this section the difference was 0.8 MB against 5.3 MB.
pandas 3's `str` type shows no difference, but write it anyway out of habit.

## 2. Taking the file size for the memory size

A 61 MB CSV took 96 MB in memory; the same file took 252 MB with `object`
storage. Do not look at the file and say "it fits"; read a few thousand rows,
measure the bytes per row, then multiply by the number of rows.

## 3. Looking at the end and forgetting the peak

When an operation is over the table may be 4 MB, but it may have reached
15 MB while running. A program crashes at the peak, not at the end. For heavy
operations, look at the peak with `tracemalloc`.

## 4. Using `tracemalloc` to measure a table

`tracemalloc` does not see pandas 3's text columns; for a text-heavy table it
gives far too small a number. For a table, `memory_usage(deep=True)`.

## 5. Measuring time once

The first run is often slow: the file is not yet in the operating system's
cache, modules are loading. Measure several times and look at the smallest
or the median.

## 6. Comparing different computers

"0.8 seconds on mine, 2 seconds on yours" says nothing. Compare two methods
on the **same** computer, **one after the other**; give the result as a
ratio.

## 7. Mixing up units

There is about a 5% difference between `1024**2` and `10**6`; with big
numbers, gigabytes drift. Pick a unit once in a project and always use it.

## 8. Not counting copies

`df2 = df[df["city"] == "Istanbul"]` is a new table. The old `df` is still
in memory. Let go of a big table you will not use again with `del df`.

## 9. Forgetting the index

An index built from mixed numbers is 8 more bytes per row. Over millions of
rows that is megabytes too.
