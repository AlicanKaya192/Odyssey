Find each employee's **level** in the company: the person at the top with
no manager is 0, those directly below are 1, those below them 2.

Columns: `id`, `name`, `level`. Sort by `level` first, then by `id`.

```
id  name         level
--  -----------  -----
1   Ada Kilic    0
2   Bora Yilmaz  1
5   Emre Sahin   1
3   Ceren Aksoy  2
...
```

Every employee in the `employees` table has a `manager_id`. This query
has to be written without knowing how many levels there are: a
recursive `WITH` starts from the person at the top, goes one level down
at every step, and stops when nobody new comes in.
