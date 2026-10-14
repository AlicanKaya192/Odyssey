`leaked(examples, test)` should return, smallest first, the ids of the test
messages that are the same as one of the example texts put into the
prompt. Before comparing, remove leading and trailing spaces from the
texts on both sides and turn them into lower case. The test items are
`{"id", "text"}` dictionaries.

**Expected output:**

```
[3, 7]
```
