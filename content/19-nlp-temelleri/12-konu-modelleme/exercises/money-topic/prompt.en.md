The 8-topic NMF is ready (`nmf`, `W`). `main_topic(category)` should look at
the heaviest topics of the tickets in that category, find the most common
topic and return `[the topic's first 3 words, the share of tickets in that
topic]` (share with 3 places). Do the two categories land in the same
topic?

**Expected output:**

```
billing ['card paid credit', 0.453]
refund ['card paid credit', 0.815]
```
