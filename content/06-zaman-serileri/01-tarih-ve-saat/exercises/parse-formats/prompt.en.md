Four dates arrive from four different systems, each in its own format:

| Text | Source | Format |
|---|---|---|
| `09.03.2024` | A form in Turkey | day.month.year |
| `12/25/2023` | A system in the US | month/day/year |
| `2024-07-01 08:15` | A database | ISO 8601 |
| `1 February 2024` | An e-mail | day, month name, year |

**What to do:**

1. Turn each text into a `datetime`: write the right format with `strptime`
   for the first two and the last one, and use `fromisoformat` for the ISO
   one.
2. Put all four in a list and **sort** it.
3. Print each date of the sorted list with `isoformat()`, one per line.

**Expected output:**

```
2023-12-25T00:00:00
2024-02-01T00:00:00
2024-03-09T00:00:00
2024-07-01T08:15:00
```

They were all translated into one language, ISO 8601, and now they sort
correctly. This is how dates from different sources are combined: first turn
them all into one type, then compare.
