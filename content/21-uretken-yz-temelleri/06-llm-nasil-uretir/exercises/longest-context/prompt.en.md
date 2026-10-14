`next_word(dialogues, context)` should build the lesson's model at a small
scale. Split every dialogue (text separated by spaces) into tokens; at every
position take the previous 1–7 tokens as the context and count the token that
follows. Then find the longest familiar ending of the given `context` text and
return the token that most often follows that context (on a tie, the one that
comes first alphabetically).

**Expected output:**

```
hello
hello
```
