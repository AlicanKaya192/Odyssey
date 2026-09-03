Words you will keep running into when you read about data science or open a
library's documentation. You do not need to memorise them now; come back here
when you get stuck.

## The shape of data

| Term | What it means |
|---|---|
| **Record / row** | Everything known about one entity: a student, an order, a day |
| **Feature / column** | The same attribute measured across every record: score, city, price |
| **Observation** | The same thing as a record. The name statistics brought along |
| **Dataset** | All the rows and columns together; a table |
| **Shape** | How many rows, how many columns. `(800, 5)` = 800 records, 5 features |

Three names for the same thing is confusing, but there is a reason: data
science sits where statistics, databases and software meet, and each brought
its own vocabulary.

## Kinds of variable

**What kind** of value a column holds decides what you can do with it.

| Kind | Example | What you do |
|---|---|---|
| **Numeric** | score, price, age | average, total, difference |
| **Categorical** | city, gender, class | count, group |
| **Ordinal** | low / medium / high | has an order, but no measurable gap |
| **Datetime** | 2026-03-14 | ranges, day differences, grouping by month |
| **Text** | comment, description | search, length, parsing |

**A common mistake:** a postcode or a student number looks numeric but is
categorical. There is no such thing as an average postcode.

## Summary statistics

Measures that reduce a numeric column to a single sentence:

| Measure | What it tells you |
|---|---|
| **Mean** | The total divided by the number of records |
| **Median** | The middle value once you sort them |
| **Mode** | The value that appears most often |
| **Min / max** | The extremes |
| **Standard deviation** | How far the values spread from the mean |

**Why have both mean and median?** Because the mean is pulled by extreme
values. If five salaries are 30, 32, 35, 33 and 900 thousand, the mean is 206
thousand — which is nobody's salary. The median says 33 thousand and
describes the situation correctly.

When the mean and the median of a column are **far apart**, there are extreme
values in there.

## Data quality

| Term | What it means |
|---|---|
| **Missing value (NaN)** | The cell is empty. Not zero — "unknown" |
| **Outlier** | A value far from the rest. It can be an error or it can be real |
| **Duplicate** | The same row entered twice |
| **Inconsistency** | The same thing written differently: `"Ankara"`, `"ankara"`, `"ANKARA"` |

All of these exist in real data. There is no such thing as clean data; there
is data that has been cleaned.

## Operations

| Term | What it means |
|---|---|
| **Filter** | Keep the rows that match a condition |
| **Selection** | Take particular columns |
| **Group by** | Split the rows into buckets by a column |
| **Aggregation** | Reduce each bucket to a single number |
| **Join / merge** | Put two tables side by side on a shared column |
| **Sort** | Order the rows by a column |

These six cover nearly all data work. SQL has the same ones (`WHERE`,
`SELECT`, `GROUP BY`, `JOIN`, `ORDER BY`) — even the names look alike,
because they are the same ideas.

## File formats

| Format | When |
|---|---|
| **CSV** | Comma-separated plain text. Opens everywhere, the most common |
| **Excel** (.xlsx) | Multiple sheets, formatting. Common in business |
| **JSON** | For nested structures. Usually what an API gives you |
| **Parquet** | Compressed, column-oriented. Fast on large data |
| **SQL** | Pulled out of a database with a query |

CSV is enough to start with. The plain text files you read in the `Working
with Files` section were a simple version of this.

## Libraries

| Library | For what |
|---|---|
| **NumPy** | Arrays of numbers, arithmetic, speed |
| **pandas** | Tables: reading, cleaning, grouping |
| **Matplotlib** | Drawing charts |
| **scikit-learn** | Machine learning models |

pandas is built on top of NumPy; Matplotlib works with both. scikit-learn is
the subject of the next path.
