`part_tokens(parts)` should find the token count of every part in the
dictionary with `count_tokens` from the read-only `llm_client.py` and
return a list of `[name, tokens]` pairs: token count from largest to
smallest, names in alphabetical order on ties.

**Expected output:**

```
role 9
labels 8
format 7
input 7
```
