`missing_fields(plan, required)` should return, in the same order, the
names in `required` that are **absent or empty** in the plan (a value such
as `False`, `""` or `[]`).

**Expected output:**

```
written_permission
window
emergency_contact
```
