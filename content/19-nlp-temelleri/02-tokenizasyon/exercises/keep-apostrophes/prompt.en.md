`tokenize(text)` should keep words such as "can't" and "it's" as one token: the
pattern is `\w+(?:'\w+)?|[^\w\s]`. Do not lowercase the text; split it as it
is.

**Expected output:**

```
I|can't|believe|it's|here|!
Don't|stop|.
```
