Common mistakes in pagination loops and their symptoms.

| Symptom | Cause | Fix |
|---|---|---|
| The loop never ends | Wrong stopping condition (looking at a field other than `next`) | Write the condition from the documentation; use a bounded `for` |
| The same page keeps coming | `page` is not increased or not put in `params` | `page += 1` inside the loop; look at `r.url` |
| The last records are missing | `break` before adding the last page | `extend` first, then check whether to stop |
| The first page twice | The loop starts at 1 and the first page was also fetched before | Fetch the first page either in the loop or outside it, not both |
| `[[...], [...]]` in the list | `append` instead of `extend` | Use `extend` to add a page's items |
| Asked for more than 20, got 20 | The server's page size limit | Look at `meta.per_page` and accept the limit |
| Filtering is lost when following links | `?page=` built by hand instead of `next` | Use the `next` address the server gives, as it is |

## `append` versus `extend`

```python
books = []
books.append(["Emma", "Dune"])   # [['Emma', 'Dune']]   -> one item: a list
books = []
books.extend(["Emma", "Dune"])   # ['Emma', 'Dune']     -> two items
```

## Count how many requests you send

You can work out in advance how many requests a pagination loop will send:
`total / page_size`, rounded up. 23 books with pages of 5 → 5 requests; pages
of 20 → 2 requests. If you see a loop sending many requests, try a bigger page
size first.
