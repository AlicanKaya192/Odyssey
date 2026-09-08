The comparisons you can use inside `WHERE`. The first four are enough for
this section; the rest belong to the next one, but they are listed here
because seeing them in one place helps.

## Comparing numbers and text

| Operator | Meaning | Example |
|---|---|---|
| `=` | equal | `price = 450` |
| `<>` | not equal | `category <> 'Display'` |
| `<` | less than | `stock < 5` |
| `>` | greater than | `price > 1000` |
| `<=` | less or equal | `stock <= 0` |
| `>=` | greater or equal | `price >= 1000` |

`!=` works too and does the same thing as `<>`. The standard one is `<>`;
teams usually pick one and stay with it.

## Logical connectors

| Operator | Meaning |
|---|---|
| `AND` | both conditions must hold |
| `OR` | at least one must hold |
| `NOT` | inverts a condition |

**Precedence:** `NOT` → `AND` → `OR`. So `AND` runs before `OR`.

## Common mistakes

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Writing <code>==</code></span><span class="anat-body">It does not exist in SQL. Equality is a single <code>=</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Double quotes</span><span class="anat-body"><code>"Display"</code> is not text, it is an <b>object name</b>. Text goes in single quotes.</span></div>
    <div class="anat-row"><span class="anat-label">Quoting a number</span><span class="anat-body"><code>price &gt; '1000'</code> works, but the server converts on every row. Write a number as a number.</span></div>
    <div class="anat-row"><span class="anat-label">AND/OR with no parentheses</span><span class="anat-body">When both appear, add parentheses — even when it would work anyway.</span></div>
  </div>
</figure>

## What is coming in the next section

These also live inside `WHERE`, but they are a topic of their own:

| Operator | What it does |
|---|---|
| `BETWEEN` | between two values (`price BETWEEN 500 AND 2000`) |
| `IN` | one of a list (`category IN ('Display', 'Accessory')`) |
| `LIKE` | a text pattern (`name LIKE 'K%'`) |
| `IS NULL` | is the value missing |

`IN` in particular is the short form of the long `OR` chains in this
section.
