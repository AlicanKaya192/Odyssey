Write the function `missing_sections(doc, required)` that finds the missing sections in a design document:

- `doc` is a string; section headings are lines starting with `"## "`.
- The heading's name is what comes after `"## "`, with spaces trimmed.
- Return the names in the `required` list that don't appear as headings in the document, in the same order.

**Expected output:**

```
['Model', 'Monitoring']
[]
```
