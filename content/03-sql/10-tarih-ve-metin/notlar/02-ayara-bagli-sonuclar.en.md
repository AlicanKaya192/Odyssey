The same query can give two different results on two different servers.
It raises no error either; only the result changes. This note collects
the setting-dependent behaviour measured in this section and how to pin
each one down.

## Which settings

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Language setting (collation)</span><span class="anat-body">How letters are compared and turned to capitals or small letters. On this machine <code>Turkish_CI_AS</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Session language</span><span class="anat-body">Which language month and day names are written in. On this machine <code>us_english</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Date format</span><span class="anat-body">Whether a text like <code>'03/04/2026'</code> is read day-first or month-first (<code>SET DATEFORMAT</code>).</span></div>
    <div class="anat-row"><span class="anat-label">First day of the week</span><span class="anat-body">What <code>DATEPART(weekday, ...)</code> returns. On this machine <code>@@DATEFIRST = 7</code> (Sunday).</span></div>
  </div>
</figure>

They are all chosen at installation or in the session; your server may be
different.

## 1. Date text

| Written as | Setting | Day read |
|---|---|---|
| `'03/04/2026'` | `dmy` | April 3 |
| `'03/04/2026'` | `mdy` | March 4 |
| `'2026-03-04'` → `DATETIME` | `dmy` | **April 3** |
| `'2026-03-04'` → `DATE` | `dmy` | March 4 |
| `'20260304'` | any setting | March 4 |

**Pinning it down:** `'YYYY-MM-DD'` for `DATE`, `'YYYYMMDD'` for
`DATETIME`. The slashed form is never used.

## 2. Month and day names

`DATENAME(month, '2026-03-14')` gave `March` on this server, and
`DATENAME(weekday, ...)` gave `Saturday`. In a Turkish session the same
query gives `Mart` and `Cumartesi`.

**Pinning it down:** give the culture explicitly.

```sql
FORMAT(d, 'MMMM yyyy', 'tr-TR')   -- Mart 2026
FORMAT(d, 'MMMM yyyy', 'en-US')   -- March 2026
```

## 3. The weekday number

`DATEPART(weekday, '2026-03-14')` gave **7** on this server: the week
starts on Sunday, so Saturday is the seventh day. With `SET DATEFIRST 1`
starting the week on Monday, the same day became **6**.

The setting also changes along with the session language: after
`SET LANGUAGE Turkish`, `@@DATEFIRST` became 1 by itself. So without
touching the query at all, only changing the session language changes
the result of a query that filters weekends.

**Pinning it down:** in a query that decides by the day number (like
filtering weekends) do not rely on the setting; either set it yourself at
the start of the query with `SET DATEFIRST 1`, or work with date ranges
instead.

## 4. The Turkish I

| Expression | Turkish setting | Latin setting |
|---|---|---|
| `UPPER('istanbul')` | `İSTANBUL` | `ISTANBUL` |
| `LOWER('ISTANBUL')` | `ıstanbul` | `istanbul` |
| `WHERE city = 'istanbul'` | **0 rows** | 2 rows |
| `WHERE city LIKE 'ist%'` | **0 rows** | 2 rows |

In Turkish the small form of `I` is `ı`, and the capital of `i` is `İ`.
A Turkish-set server follows that, so a search for `istanbul` cannot find
a record written `Istanbul`.

**Pinning it down:** state the language setting in the comparison.

```sql
WHERE city COLLATE Latin1_General_CI_AS = 'istanbul'   -- 2 rows
```

## 5. Letter case and keys

On this server comparisons ignore letter case (`CI`): in the previous
section `w1` and `W1` counted as the same primary key. On a server that
tells capitals apart (`CS`) they would be different.

## This application's exercises

The expected results were produced on a Turkish-set server, but every SQL
exercise was **also run on a Latin-set database** and all of them gave the
same result. So whatever language your server was installed in, a correct
solution passes.

## The question to ask

When you write a query, ask yourself: **"Does this result depend on the
server's language, date format or week setting?"** If it does, state the
setting explicitly inside the query.
