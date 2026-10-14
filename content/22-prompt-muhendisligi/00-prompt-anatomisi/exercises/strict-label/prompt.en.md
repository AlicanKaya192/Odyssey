`parse_label(text, labels)` should parse the model's answer strictly:
remove leading and trailing spaces, turn it into lower case, remove a
final `.` and `!`. If the result is in the `labels` list return it,
otherwise return `"needs_review"`. Do not search the text for a
category name.

**Expected output:**

```
'Refunds.' refunds
' payment\n' payment
'Returns?' needs_review
'It is shipping.' needs_review
```
