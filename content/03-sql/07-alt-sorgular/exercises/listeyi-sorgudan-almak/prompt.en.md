Bring back the products of suppliers based in Istanbul.

One column: `name`. Sort alphabetically.

```
name      
----------
Desktop   
Laptop    
Microphone
```

In the third section you wrote the `IN` list by hand. Here you **will
not**: take the codes of the Istanbul suppliers from the `suppliers` table
with a subquery.

The reason is the same: type the codes in and the query goes quietly wrong
as soon as a supplier moves.

The inner query must return **one column** — that is where `IN` takes the
value it compares.
