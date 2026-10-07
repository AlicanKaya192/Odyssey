Words that come up often in big data articles, lecture slides and job
adverts. Next to each one, where the track covers it in detail.

## Hardware

| Term | Meaning |
|---|---|
| **Memory (RAM)** | The fast but small and temporary area where a program works right now. |
| **Disk (SSD, HDD)** | The large area where files live permanently; slower than memory. |
| **Page file** (*swap*) | The part of memory the operating system moves to disk when memory is full. The program does not crash but slows down a lot. |
| **Core** | One of the units of a processor that can do work at the same time. 8 cores, 8 jobs at once (Section 10). |
| **Node** | A single computer in a cluster. |
| **Cluster** | Computers working together on one job (Sections 12–13). |

## Concepts

| Term | Meaning |
|---|---|
| **Out-of-core** | Processing data that does not fit in memory piece by piece (Section 3). |
| **Scale up** | A single, more powerful machine. |
| **Scale out** | More machines. |
| **Distributed processing** | Splitting the work across several machines (Sections 12–13). |
| **Batch processing** | Processing accumulated data in bulk at set intervals. |
| **Streaming** | Processing data the moment it arrives (Section 14). |
| **Columnar format** | A file format that stores data column by column rather than row by row; Parquet (Sections 4–5). |
| **Partitioning** | Splitting data into separate files by a column (Section 6). |
| **Sampling** | Working with a representative part of the data instead of all of it (Section 9). |

## The Vs of big data

| V | Question | Example |
|---|---|---|
| **Volume** | How much? | All orders from 5 years, 2 TB |
| **Velocity** | How fast does it arrive? | 10 000 clicks a second |
| **Variety** | In what form? | Tables + JSON + images + text |
| **Veracity** | How trustworthy? | Faulty sensor readings |
| **Value** | Is it useful? | Which products are bought together? |

## Tools

| Tool | What it is for | On the track |
|---|---|---|
| **pandas** | Working with a table that fits in memory | Every section |
| **pyarrow** | Reading and writing Parquet, columnar memory | Sections 4–6 |
| **DuckDB** | SQL on top of files, on one machine | Sections 7–8 |
| **dask** | A pandas-like table processed in pieces and in parallel | Section 11 |
| **Hadoop** | Distributed storage (HDFS) and MapReduce | Section 12 |
| **Spark** | In-memory distributed processing on a cluster | Section 13 |
| **Kafka** | A messaging system that carries streaming data | Section 14 |
