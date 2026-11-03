`missing_fields(record, required)` should return, in alphabetical order,
the names of required fields that are **missing or empty** in the record.
A record with missing fields leaves "who, from where?" unanswered when an
incident happens.

**Expected output:**

```
['result', 'source']
[]
```
