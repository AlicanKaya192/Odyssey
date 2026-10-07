The same information can sometimes go in the address, sometimes in the
query. Which one you choose is a design decision.

| Question | Path parameter | Query parameter |
|---|---|---|
| What does it describe? | **Which** thing (the id) | **Which part** of that thing, **in what order** |
| Example | `/books/42` | `/books?year_from=1950&page=2` |
| If not sent | The address is incomplete: another endpoint | The default value |
| How many? | Few (one or two) | As many as you like, order does not matter |

## The rule

- Information that **selects the resource** goes in the path: `/books/42`,
  `/authors/7/books`.
- Information that **filters, sorts or pages the result** goes in the
  query: `?author=`, `?sort=year`, `?page=2`.
- Because a query is optional, adding a new filter does not break old
  clients; adding a new part to the path does.

## Examples

| Request | The right place |
|---|---|
| Book 42 | path: `/books/42` |
| Books after 1950 | query: `/books?year_from=1950` |
| Austen's books | both work: `/authors/austen/books` or `/books?author=Austen` |
| Sorted by year | query: `/books?sort=year` |
| The second page | query: `/books?page=2` |

## Keep in mind

> The path answers "which one?", the query answers "how?".
