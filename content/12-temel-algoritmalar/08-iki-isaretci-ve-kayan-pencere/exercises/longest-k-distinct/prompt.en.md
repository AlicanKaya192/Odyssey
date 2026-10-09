Write the function `longest_k_distinct(text, k)` **with a variable window**:
it returns the length of the longest consecutive piece of the text containing
**at most `k` distinct letters**.

- `longest_k_distinct("eceba", 2)` → `3` (`"ece"`)
- `longest_k_distinct("aaabbcc", 2)` → `5` (`"aaabb"`)

Keep the counts of the letters in the window in a dictionary. Move the right
end on; when the number of distinct letters goes above `k`, remove from the
left (delete a letter from the dictionary when its count drops to zero) and
move the left end on.

**Expected output:**

```
3
5
0
```
