The commands in this section are easy. What is hard is not running them
wrongly.

What follows are not rules but **habits**: each takes a few seconds, and
each one prevents an accident that has really happened.

## 1. A SELECT first, with the same WHERE

```sql
SELECT * FROM products WHERE category_code = 'ACC';
```

You see on screen exactly which rows are about to change. If that is
right, you replace the `SELECT *` part with `UPDATE ... SET ...` and
leave the `WHERE` alone.

This one habit prevents the large majority of `UPDATE` and `DELETE`
mistakes, because most mistakes are not in the command but in the
**condition**.

## 2. Look at the row count

The server tells you how many rows it touched after every write. Make
reading that number a **habit**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Expected 1, got 40</span><span class="anat-body">The condition did not narrow enough. If you are in a transaction, <code>ROLLBACK</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Expected 1, got 0</span><span class="anat-body">The condition caught nothing. A typo, or the wrong value.</span></div>
    <div class="anat-row"><span class="anat-label">What you expected</span><span class="anat-body">Carry on.</span></div>
  </div>
</figure>

## 3. Do the dangerous work inside a transaction

```sql
BEGIN TRANSACTION;

DELETE FROM orders WHERE order_date < '2020-01-01';

SELECT COUNT(*) FROM orders;   -- does that look right?

ROLLBACK;
```

If the number is what you expected, you change the `ROLLBACK` to a
`COMMIT` and run it again. If it is not, nothing happened.

**One warning:** an open transaction holds locks on the rows it touched.
Somebody else's query starts waiting on them. Leaving a transaction open
and going for coffee is a real problem — do not walk away from a
transaction you opened.

## 4. Use the key in your WHERE

```sql
-- fragile
UPDATE customers SET city = 'Ankara' WHERE name = 'Nova Retail';

-- solid
UPDATE customers SET city = 'Ankara' WHERE id = 1;
```

Filtering by name changes two rows the day a second row carries the same
name. A primary key points at exactly one row.

If you have to use the name, look at how many rows it catches with a
`SELECT` first.

## 5. Before deleting: should it really be deleted?

In most systems rows are not deleted but **marked**:

```sql
-- instead of deleting
UPDATE orders SET status = 'cancelled' WHERE id = 1006;
```

This is called a *soft delete*. Its advantage is that it can be undone
and the history is not lost; its price is that from then on every query
needs a "not cancelled" condition.

The decision depends on the case, but that is the question to ask before
you say "delete".

## 6. Deleting one row is not enough

When you delete an order, what happens to its items?

The links in this section's schema are not declared, so the server says
nothing: the order goes, its items stay, and they point at an order that
no longer exists. Nobody notices, because the only way to find them is to
go looking for an order that is not there.

These are called **orphan rows**. There are two answers:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">By hand</span><span class="anat-body">Delete the child rows first, then the parent. Remembering the order is up to you.</span></div>
    <div class="anat-row"><span class="anat-label">Leave it to the server</span><span class="anat-body">Declare the link; the server either <b>refuses</b> the delete in the wrong order or removes the children itself.</span></div>
  </div>
</figure>

The second one is the subject of the next section.

## 7. A backup

All of the above can fail. Taking a backup before a bulk change on
production data is the dullest and most important item on this list.

## In short

<figure class="fig">
  <div class="flow">
    <span class="node">rehearse with SELECT</span>
    <span class="arrow">→</span>
    <span class="node">BEGIN TRANSACTION</span>
    <span class="arrow">→</span>
    <span class="node">UPDATE / DELETE</span>
    <span class="arrow">→</span>
    <span class="node">check the row count</span>
    <span class="arrow">→</span>
    <span class="node ok">COMMIT</span>
    <span class="arrow">/</span>
    <span class="node no">ROLLBACK</span>
  </div>
</figure>
