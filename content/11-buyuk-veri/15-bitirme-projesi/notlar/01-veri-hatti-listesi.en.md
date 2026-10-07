Questions to ask, in order, when you meet a large data set. Next to each item
is the section of the track.

## 1. Measure

- How big is the file on disk? (`os.path.getsize`)
- How much memory does a ten-thousand-row sample take per row? The estimate
  for the whole? (`memory_usage(deep=True)`, Section 1)
- How much free memory does the computer have? If the estimate is more than
  half of it, do not read in one go.

## 2. Shrink

- The smallest type that is enough for number columns (`int8`, `int32`),
  `category` for repeated text (Section 2).
- Do not read columns you do not need at all (`usecols`, `columns` in
  Parquet).

## 3. Choose the format

- If it will be queried every day, convert the CSV to Parquet once
  (Sections 4, 5).
- Convert a big file piece by piece (`chunksize` + `ParquetWriter`,
  Section 3).
- Compression: `zstd` is small, `snappy` is fast.

## 4. Partition

- Do questions always start with the same column (month, city)? Split into
  folders by that column (Section 6).
- Do not produce tiny files: each partition should have a reasonable number
  of rows.

## 5. Choose the tool

| Situation | Tool |
|---|---|
| Fits in memory easily | pandas |
| SQL on files, one machine | DuckDB (Sections 7, 8) |
| pandas syntax, bigger than memory | dask (Section 11) |
| Many machines | Spark (Section 13) |
| Data arrives live | Streaming: windows, Kafka (Section 14) |

## 6. Check

- Work out the result another way (partial totals + combining, Section 12).
- Compare decimals with a small tolerance, not `==`.
- Check row counts: the same before and after converting?

## 7. Speed or exactness?

- A quick idea: a sample (Section 9), an approximate count of different
  values.
- A result that will be published: the exact query.
