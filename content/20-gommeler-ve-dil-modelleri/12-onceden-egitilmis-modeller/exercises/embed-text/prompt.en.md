`embed_text(text, vectors)` should lowercase the text and split it on spaces;
return the average of the vectors of the words found in the `vectors`
dictionary with 3 places. If no word is known, zeros of the vector's
length.

**Expected output:**

```
[0.5, 0.5]
[1.0, 0.5]
[0.0, 0.0]
```
