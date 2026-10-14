`check_values(template, values)` should find the names of the `{{name}}`
placeholders in the template with the given `SLOT` and return `[missing
names, unused names]`: missing are those in the template but not in
`values`; unused are those in `values` but not in the template. Both
lists in alphabetical order.

**Expected output:**

```
[['message', 'order_id'], ['order']]
[[], []]
```
