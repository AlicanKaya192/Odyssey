Ideas for repeating this project with your own data or at a larger scale.

## With your own data

- Open data sets: journey or sensor data published by cities and transport
  agencies are often CSVs of millions of rows. Apply the same pipeline:
  measure, shrink, convert to Parquet, partition, query, check.
- First write down which questions you will ask. The partitioning column
  comes from the questions.

## A larger scale

| What changes | What happens in the pipeline |
|---|---|
| Data a few times the memory | Converting stays piece by piece; queries with DuckDB |
| Data at the limit of the disk | Choose columns, compress, archive old partitions |
| Data beyond one machine | The same steps with dask or Spark |
| New data every day | Add only the new day's partition; do not rewrite the old ones |
| Live data | Kafka + windows; write to the lake at the end of the day |

## New data every day: incremental loading

In the project we converted the whole year again every night. A real pipeline
processes only the **new** day and adds it to the lake as a new file:

```python
new_day.to_parquet("lake/month=2024-12/part-31.parquet", index=False)
```

With the `lake/*/*.parquet` pattern DuckDB sees the new file by itself. The
old files are not touched; this is both fast and safe (a write that stops
halfway does not damage old data).

## A pipeline you can run again

- Every step should give the same output for the same input; running a step a
  second time should do no harm (the idempotence from Section 14).
- Keep intermediate files under the step's name; if a step fails, continue
  from there, not from the start.
- Print the row count after every step; stop if the number changes
  unexpectedly.

## What you can learn from here

- **Cloud storage:** reading Parquet files in storage such as S3 with DuckDB.
- **Table formats:** Delta Lake, Apache Iceberg: they add updates, deletes and
  versions to Parquet lakes.
- **Workflow tools:** tools such as Airflow run the pipeline's steps in order
  every night and report the one that fails.
