`context_share(doc_id, doc_ids)` should work with the articles in the
read-only `doc_data.py`: find with `count_tokens` the token count of the
text of article `doc_id` and the total tokens of the texts of all
articles in `doc_ids`. Return `[one, all, one / all]`; the share rounded to
2 places.

**Expected output:**

```
[94, 361, 0.26]
[50, 361, 0.14]
```
