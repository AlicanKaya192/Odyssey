`per_category(version)` should compare the `RECORDED[version]` answers in
the read-only `shop_data.py` with the labels of `TICKETS` and return, as a
dictionary, the number of messages per category where the cleaned answer
(`strip`, `lower`, final `.` and `!` removed) is right (keys in the order
of `LABELS`).

**Expected output:**

```
v1 [6, 7, 4, 8, 6]
v2 [8, 8, 6, 7, 7]
```
