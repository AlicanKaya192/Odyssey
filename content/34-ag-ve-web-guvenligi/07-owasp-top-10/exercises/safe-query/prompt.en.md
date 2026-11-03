A small `users` table is ready in memory. `city_of(name)` should
return the person's city, or `"unknown"` if there is no such person. The
starter code builds the query by joining text and breaks on a person with
`'` in their name. Make the query **parameterised**:
`conn.execute("... WHERE name = ?", (name,))`.

**Expected output:**

```
Istanbul
Izmir
Ankara
unknown
```
