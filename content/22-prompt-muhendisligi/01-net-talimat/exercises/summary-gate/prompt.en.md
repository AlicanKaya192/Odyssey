`summarize(reviews)` should have each review summarized with a separate
call: create `ChatClient(SCRIPT)`; for each review send `[system, user]`
(`SYSTEM` and `wrap("review", review)`, `max_tokens=40`). Check every
answer with the given `check(reply.text, RULES)`. Return `[texts of the
answers that passed the rules, the list of failed rules of every
answer]`.

**Expected output:**

```
1
ok
['max_words']
['must_include']
```
