The `users` and `posts` tables are ready. `report(user_id)` should
first find the user's name, then return the titles (`title`) of the posts
written under that name as a list; `[]` if there is no such user. The
starter code does the first query with a parameter but adds the name it
read from the database to the second query **as text**, and it breaks on
`O'Brien`.

**Expected output:**

```
['hello']
['notes', 'ideas']
[]
```
