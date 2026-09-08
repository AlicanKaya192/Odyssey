A one-page reference for `LIKE`, `IN` and `BETWEEN`.

## LIKE patterns

| Pattern | Matches | Does not match |
|---|---|---|
| `'K%'` | Klavye, Kablo, K | Fare |
| `'%uk'` | Kucuk, uk | ukulele |
| `'%la%'` | Klavye, lamba, la | Fare |
| `'F_re'` | Fare, Fire | Fre, Faare |
| `'____'` | anything exactly four characters long | three or five characters |

`%` also matches zero characters: the pattern `'K%'` finds the one-letter
text `K` as well.

## Square brackets: specific to SQL Server

T-SQL also has character sets. They are not in standard SQL and do not
carry over to other databases.

| Pattern | Meaning |
|---|---|
| `'[KM]%'` | starting with K or M |
| `'[A-F]%'` | starting with a letter between A and F |
| `'[^K]%'` | not starting with K |

## Searching for the wildcard itself

```sql
WHERE aciklama LIKE '%50!%%' ESCAPE '!'
```

The character you choose with `ESCAPE` turns whatever follows it into
**literal text**. `!%` is a real percent sign; the last `%` is still a
wildcard.

You choose the escape character; anything that does not occur in the text
will do.

## A note on speed

| Pattern | Can an index be used |
|---|---|
| `'K%'` | **yes** — the beginning is known |
| `'%K'` | no |
| `'%K%'` | no |

A leading `%` means the server cannot know where to start; it has to look
at every row. You cannot tell on small tables; on large ones it is one of
the most common causes of slowness.

## IN

```sql
WHERE kategori IN ('Ekran', 'Yazilim')
```

Is exactly the same as:

```sql
WHERE kategori = 'Ekran' OR kategori = 'Yazilim'
```

- The list **cannot be empty**: `IN ()` is a syntax error.
- The list can also be a **subquery**: `IN (SELECT kod FROM tedarikciler)`.
  That belongs to the subqueries section.
- `NOT IN` together with `NULL` **always** gives an empty result; the
  details are in the NULL note.

## BETWEEN

```sql
WHERE fiyat BETWEEN 500 AND 3000
```

Is exactly the same as:

```sql
WHERE fiyat >= 500 AND fiyat <= 3000
```

- **Both ends are included.** If you need them excluded, do not use
  `BETWEEN`.
- **The smaller value goes first.** `BETWEEN 3000 AND 500` raises no error
  and returns nothing.
- It works on dates too, but with care: write
  `BETWEEN '2026-01-01' AND '2026-01-31'` and everything **after** midnight
  on the 31st falls outside. On date-time columns
  `>= start AND < end` is safer.

## Which one, when

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Specific values</span><span class="anat-body"><code>IN</code> — three categories, five cities, two status codes</span></div>
    <div class="anat-row"><span class="anat-label">A numeric or date range</span><span class="anat-body"><code>BETWEEN</code>, or <code>&gt;=</code> and <code>&lt;</code> when a bound must be excluded</span></div>
    <div class="anat-row"><span class="anat-label">Part of some text</span><span class="anat-body"><code>LIKE</code></span></div>
    <div class="anat-row"><span class="anat-label">Whether a value exists</span><span class="anat-body"><code>IS NULL</code> / <code>IS NOT NULL</code></span></div>
  </div>
</figure>
