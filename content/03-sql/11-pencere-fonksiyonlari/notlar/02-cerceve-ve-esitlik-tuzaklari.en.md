Most mistakes with window functions raise no error message: the query
runs, the result looks reasonable, and it is wrong. This note collects
the traps measured in this section and the fix for each one.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ROW_NUMBER on ties</span><span class="anat-body">Add a column that tells rows apart to the order.</span></div>
    <div class="anat-row"><span class="anat-label">The default frame</span><span class="anat-body">For a running total, write <code>ROWS UNBOUNDED PRECEDING</code>.</span></div>
    <div class="anat-row"><span class="anat-label">LAST_VALUE</span><span class="anat-body">Open the frame up to the end of the group.</span></div>
    <div class="anat-row"><span class="anat-label">Filtering afterwards</span><span class="anat-body">Filter in the inner query, before numbering.</span></div>
    <div class="anat-row"><span class="anat-label">Whole-number average</span><span class="anat-body">Convert to <code>DECIMAL</code> before averaging.</span></div>
    <div class="anat-row"><span class="anat-label">The result's order</span><span class="anat-body">A separate <code>ORDER BY</code> at the end of the query.</span></div>
  </div>
</figure>

## 1. ROW_NUMBER on ties

Two products have a stock of 99. The same `ROW_NUMBER() OVER (ORDER BY
stock DESC)` was run in two different queries:

| Query | Number 1 | Number 2 |
|---|---|---|
| ending in `ORDER BY stock DESC, name` | Antivirus | Office Suite |
| with no `ORDER BY` at the end | Office Suite | Antivirus |

Same data, same window, different result. The server has to pick an
order among ties, and that pick depends on the rest of the query.

For jobs like "one product from each category" this means the query can
bring back a different product each time it runs.

**Fix:** make the order tie-free — `ORDER BY stock DESC, name` or
`ORDER BY stock DESC, id`. `RANK` and `DENSE_RANK` do not fall into this
trap, because they give ties the same number anyway.

## 2. The default frame

Writing `OVER (ORDER BY ...)` without a frame means "from the start up to
**this value**". On order lines with `ORDER BY order_id`:

| order_id | line | default | `ROWS UNBOUNDED PRECEDING` |
|---|---|---|---|
| 1001 | 900.00 | **1815.00** | 900.00 |
| 1001 | 440.00 | **1815.00** | 1340.00 |
| 1001 | 475.00 | 1815.00 | 1815.00 |

The three rows with the same `order_id` counted as "the same value" and
went in together. The same happens in date order: if two orders are on
the same day, both show the day's total.

**Fix:** write the frame explicitly for a running total and split the
ties: `ORDER BY order_id, product_id ROWS UNBOUNDED PRECEDING` —
measured, 900, 1340, 1815.

## 3. LAST_VALUE

With the ACC products in price order, `LAST_VALUE(name) OVER (ORDER BY
price)` gave the row's **own name** on every row. Because the default
frame ends at that row, the end of the frame is the row itself.

**Fix:** `LAST_VALUE(name) OVER (ORDER BY price ROWS BETWEEN UNBOUNDED
PRECEDING AND UNBOUNDED FOLLOWING)` → Microphone on every row. Or
reverse the order and use `FIRST_VALUE`; it does not fall into this trap,
because the frame starts at the beginning.

## 4. Filtering afterwards

The "each customer's largest order" query brought back **1006**
(`2400.00`) for customer 1. 1006 is a cancelled order.

| Where the filter is | Result for customer 1 |
|---|---|
| nowhere | 1006 — cancelled |
| outside: `WHERE rk = 1 AND status <> 'cancelled'` | **no row at all** — the customer dropped out |
| inside, before numbering | 1003 (`2340.00`) — right |

Filtering outside is even worse: the cancelled order took number 1 and
was then removed, so the customer has no row left.

**Fix:** choose which rows compete **before** numbering them; write the
`WHERE` in the inner query.

## 5. The whole-number average

`AVG(stock) OVER ()` gave **19** for ACC; the true value is 19.33. A
window does not change the rule that the average of whole numbers is a
whole number.

**Fix:** `AVG(CAST(stock AS DECIMAL(10,2))) OVER ()` → `19.333333`.

## 6. The order in OVER is not the result's order

`OVER (ORDER BY price DESC)` only says what the number goes by. In the
measurement the result came back in that order, but that was the
server's plan at the time.

**Fix:** if the result's order matters, write `ORDER BY` at the end of
the query.

## 7. NULL is a group too

When the number of orders per employee was ranked, the two orders with
no employee (`employee_id` `NULL`) formed a group too and took **3rd**
place.

**Fix:** if only real groups should be ranked,
`WHERE employee_id IS NOT NULL`.

## The questions to ask

When you write a window query, ask two things:

- **"Can the order column have ties?"** If it can, add a column that
  tells rows apart, and write `ROWS` for running calculations.
- **"Which rows should compete?"** Filter before numbering.
