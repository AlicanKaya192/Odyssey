Ways to keep learning after this track.

## Next in Odyssey

- **The Data Engineer route:** after Big Data, the API tracks (serving a
  pipeline's result as a service) and Docker (packaging the pipeline to run
  the same on every computer).
- **Time Series:** the windows and event time of streaming data also come up
  when forecasting time series.
- **Machine Learning:** measuring, sampling and checking apply just the same
  when choosing the data that goes into a model from a large data set.

## Trying the real tools on your own computer

| Tool | How to start |
|---|---|
| PySpark | Install Java (such as JDK 17), `pip install pyspark`, on one machine with `local[*]` |
| Kafka | A Kafka image running in a single container with Docker |
| Polars | `pip install polars`: a columnar, parallel table library similar to pandas |
| DuckDB | You already know it: there is a command-line tool too (`duckdb`) |

Running the `minispark` code from Section 13 on real Spark with
`from pyspark.sql import SparkSession` is a good first step; the differences
are in the Spark Cheat Sheet note.

## Topics you can learn from here

- **Cloud storage:** Amazon S3, Google Cloud Storage. Parquet lakes usually
  sit there; DuckDB and Spark can read the files there.
- **Table formats:** Delta Lake, Apache Iceberg. They add updates, deletes and
  versions (going back in time) to Parquet lakes.
- **Workflow tools:** Apache Airflow, Dagster. They run a pipeline's steps in
  order every night, report the one that fails, and retry.
- **Data warehouses:** BigQuery, Snowflake. Services whose servers are run by
  someone else, running SQL over terabytes (paid).
- **Stream processing:** Apache Flink, Spark Structured Streaming; the windows
  and watermarks from Section 14 are ready-made there.

## Your own project

1. Find an open data set of millions of rows (transport, weather, energy
   use).
2. First write down what you will ask.
3. Apply the pipeline from the capstone project: measure, shrink, convert to
   Parquet, partition, query with DuckDB, check two ways.
4. Note the number you measured at every step; at the end, answer "what did I
   gain" with numbers.
