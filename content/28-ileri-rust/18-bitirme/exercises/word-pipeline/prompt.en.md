Write `word_totals(spawner, lines)`. For each line, a task sends the words to the channel. A single task reads the channel and counts words in a `BTreeMap`. Return that task's `JoinHandle`.

**Expected output:**

```text
{"one": 1, "three": 3, "two": 2}
```
