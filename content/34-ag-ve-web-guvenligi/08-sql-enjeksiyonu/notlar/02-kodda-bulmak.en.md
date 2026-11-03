To find a SQL injection hole in your own code or in a code review, you do
not need to try attacks; reading the code is enough. The only thing you
look for is a place where the query text is built **by joining it with a
value that could come from the user**.

## What to look for

- `f"`, `+`, `%`, `.format(` in the text going to an `execute(` call.
- Places that prepare the query text in a variable and then call
  `execute(query)`: look at how `query` is built.
- Functions that run a "raw query" inside an ORM.
- Places where a value read from the database is used as text in another
  query (second order).

## Common excuses

| Excuse | Why it is wrong |
|---|---|
| "This value comes from a drop-down list" | A request can be written without a browser (the HTTP and HTTPS section) |
| "This value is from our own database" | The user wrote it there too |
| "Only administrators use it" | An administrator account can be taken over too |
| "We delete the quotes" | A filter forgets something; a parameter does not |
| "It is a column name, so a parameter does not work" | True; the solution is an allow list |

## Order of the fix

1. Turn the query into placeholder form and give the values in the second
   argument.
2. If a column or table name varies, map it to an allow list.
3. If there is a `LIKE`, escape the wildcards.
4. Look at what the error messages show the user.
5. Protect the fix with a test: the query must work correctly with a
   record that has a `'` in its name.

## Innocent inputs to use in tests

You do not need an attack payload to look for the hole. These inputs must
not break a correctly working query:

- Someone with an apostrophe in their name: `O'Brien`
- A name with double quotes: `Ann "Jr" Lee`
- A search with a percent sign and an underscore: `50%`, `plan_b`
- Empty text
