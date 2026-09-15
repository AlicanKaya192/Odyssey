This path went through SQL Server's query language from start to end on
an order database. Below is the answer, in order, to "what should I do
now?".

## First: a database of your own

Something that works on course data is not yet yours.

- Pick a field you know: your books, the scores of a game, the members of
  a club, your spending.
- **Design the tables yourself.** Which information goes in which table,
  what the primary key of what is, which column links to which table — on
  this path the schema came ready-made; in real life it is the hardest
  decision.
- Put the rules in from the start: `NOT NULL`, `CHECK`, `FOREIGN KEY`.
  The schema of this path had no foreign keys, and when a customer was
  deleted their orders were left orphaned.
- Then write yourself ten questions and answer each with a single query.

**The test of what you learned:** can you guess how many rows a query
will return before you see the result?

## Other database systems

The core of SQL — `SELECT`, `JOIN`, `GROUP BY`, windows, `WITH` — is
the same in almost every system. The differences are in the dialect.
Some of what you saw on this path is specific to T-SQL: `TOP`,
`GETDATE()`, `ISNULL`, `IDENTITY`, joining text with `+`, `THROW`. When
you move to PostgreSQL, MySQL or SQLite, looking up the counterparts of
these few things is enough; for example, limiting rows is written there
with `LIMIT` instead of `TOP`.

That is why the path chose portable ways of writing where it could:
`COALESCE` (instead of `ISNULL`), `CASE`, the half-open date range.

## SQL from Python

This application sends its queries from Python with `pyodbc`. The same
road is open for your own programs:

- Connect with `pyodbc` or `sqlalchemy`, run the query, fetch the rows.
- `pandas`, from the Data Science path, can read a query's result
  straight into a DataFrame (`pandas.read_sql`).
- **Do not paste a value that comes from a user into the query as
  text;** use a parameter (`WHERE id = ?`). Pasting text is the source of
  the security hole called "SQL injection".

## The execution plan

In the indexes section you measured the number of reads. SQL Server
Management Studio draws a query's **plan** — which index it used, where
it scanned. It is the first place to look at when a query is slow.

## Transactions and concurrency

On this path everything ran on its own. In a real database many people
write at the same time. The next topics: what a transaction fully means
(`BEGIN TRAN`, `COMMIT`, `ROLLBACK`), locks and isolation levels, two
people trying to change the same row.

## Design

The table design section showed the rules. The next step is **normal
forms**: not keeping the same information in two places, and why tables
get split. Databases built for reporting and analysis take the opposite
approach: the star schema.

## In this application

The Data Science path is about what to do with the data SQL pulls out;
the Machine Learning path about building models from it. SQL is the
first step of both.
