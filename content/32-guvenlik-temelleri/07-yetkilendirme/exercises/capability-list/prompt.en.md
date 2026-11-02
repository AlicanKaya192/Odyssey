`capability_list(matrix, subject)` should return everything a subject
may do as `"object:action"` texts, in alphabetical order. An empty list for
an unknown subject.

**Expected output:**

```
['grades:read', 'payroll:read']
['grades:read', 'grades:write']
[]
```
