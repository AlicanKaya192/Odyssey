`tables` is table name → list of rows (each row has `email`).
`access_report(tables, email)` should return a `"<table>: <count>"` line
for every table holding records of the person, in alphabetical order by
table name. Emails are compared regardless of case; a table with no
records is not written.

**Expected output:**

```
customers: 1
orders: 2
```
