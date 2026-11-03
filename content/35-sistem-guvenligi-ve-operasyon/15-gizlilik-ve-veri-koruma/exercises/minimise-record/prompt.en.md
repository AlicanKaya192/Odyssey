`minimise(record, allowed)` should return a **new** dict carrying only
the record's fields that are in the `allowed` list. A field in the list
but not in the record (such as `fax`) must not be added.

**Expected output:**

```
email ada@example.org
phone 555-0100
```
