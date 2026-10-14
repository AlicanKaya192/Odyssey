`scores(replies, gold, labels)` should compare the answers with the right
labels and return `[exact, valid, right]`: exact is the number of answers
equal to the right label without any cleaning; valid, the number whose
cleaned answer (`strip`, `lower`, final `.` and `!` removed) is in
`labels`; right, the number whose cleaned answer equals the right
label.

**Expected output:**

```
[1, 3, 2]
```
