`topic_heads(k)` should train `NMF(n_components=k, random_state=0,
max_iter=500)` on the ready `X`. Join each topic's **two** heaviest words with
a space and return the topics as a **sorted** list (topic numbers mean
nothing; sorting makes the result comparable).

**Expected output:**

```
account address
app page
order delivered
```
