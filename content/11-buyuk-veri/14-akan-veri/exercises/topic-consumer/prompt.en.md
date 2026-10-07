Write the payments to a `minilog` topic, read them piece by piece with
offsets, and find the revenue while removing copies.

**What to do:**

1. `topic = Topic("payments", partitions=3)`. Send every payment in the
   `payments(3_000, duplicates=True)` stream with the card as the key and the
   event itself as the value.
2. Print the number of records per partition (`end_offset`) as a list.
3. The consumer: `offsets = {0: 0, 1: 0, 2: 0}`. Read each partition until its
   end with `read(partition, offset, max_records=250)`; after every batch set
   the offset to one more than the last record's offset.
4. Print the number of records read, and the number of different payments
   after removing copies by `event_id`.
5. Print the revenue without copies (two decimals) and whether it is the same
   as the revenue of the stream without copies (`payments(3_000)`) (round
   both to two decimals).

**Expected output:**

```
[949, 949, 1199]
3097 3000
360332.69
True
```
