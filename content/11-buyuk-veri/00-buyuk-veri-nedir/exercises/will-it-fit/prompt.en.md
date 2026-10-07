Write a function that works out the most rows that fit into a computer's
memory.

You cannot give all of memory to the table: the operating system and open
programs take room too, and pandas makes intermediate copies while it
calculates. In this exercise we set aside **half of memory** for the table as
a safety margin.

**What to do:**

Write a function called `max_rows(ram_gb, columns)`:

1. Find the bytes of memory: `ram_gb * 1024**3`.
2. Set half of it aside for the table.
3. Find the bytes of one row: each column is 8 bytes.
4. Return the number of rows that fit as a **whole number** (`//`).

Examples:

- `max_rows(16, 10)` → `107374182`
- `max_rows(8, 4)` → `134217728`

About 107 million rows with 10 numeric columns fit into a 16 GB computer.
Once text columns come in, that number drops fast.
