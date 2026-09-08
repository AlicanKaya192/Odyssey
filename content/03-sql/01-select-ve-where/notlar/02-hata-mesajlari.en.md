The server's error messages are short. Here are the five you will meet in
this section and what they are trying to say.

## Invalid column name 'X'

**There is no such column.** Three possibilities, in order:

1. **A typo.** You wrote `fiyt` where `fiyat` was meant.
2. **You used double quotes.** Write `WHERE kategori = "Ekran"` and the
   server goes looking for a column named `Ekran`. Text goes in **single
   quotes**.
3. **You used a `SELECT` alias inside `WHERE`.** The server runs `WHERE`
   first; at that point the alias does not exist yet.

```sql
-- does not work
SELECT fiyat AS tutar FROM urunler WHERE tutar > 1000;
-- works
SELECT fiyat AS tutar FROM urunler WHERE fiyat > 1000;
```

## Invalid object name 'X'

**There is no such table.** Usually a typo in the table name, or you are
connected to the wrong database (the dropdown at the top in SSMS).

## Incorrect syntax near 'X'

**The statement could not be parsed.** The server does not know what to do
where it found `X`. The most common causes:

- A missing comma: `SELECT ad fiyat FROM ...`
- An extra comma: `SELECT ad, FROM ...`
- A misspelled keyword: `SELCT`, `FORM`, `WEHRE`
- An unclosed quote: `WHERE kategori = 'Ekran`

The problem may be **just before `X` rather than at `X`** — the server only
notices once it gets there.

## Conversion failed when converting the varchar value 'X' to data type int

**You compared text with a number**, as in `WHERE stok = 'bes'`. The
server tries to turn the text into a number and cannot.

## Ambiguous column name 'X'

**That name exists in two places.** It does not come up in this section
because you work with a single table; it appears once you join two tables.

---

## It can be wrong without an error

This is the dangerous case: the query runs, a result comes back, and it is
the **wrong** result. The server cannot tell you that.

The most common cause is `AND` / `OR` parentheses. The way to catch it:
**say how many rows you expect before you run it**, then look at the count
you got. If it does not match, run the condition piece by piece.
