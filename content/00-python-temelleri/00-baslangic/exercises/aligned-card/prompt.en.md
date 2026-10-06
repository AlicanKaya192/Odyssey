Draw this card **exactly**:

```
+------------------+
| Odyssey          |
| Lesson: 00       |
| Score:  100      |
+------------------+
```

Rules:

- Do not type the score (`100`) yourself: let `print` calculate it from
  `7 * 12 + 16`.
- The `|` marks on the right edge must line up. In this exercise the
  output is compared **space for space**.

The score line is the tricky part: when you give `print` pieces separated
by commas, one space goes in between each of them. Count those spaces too
to line up the edge.

> Watch out: there must be no extra spaces at the end of the lines. Every
> line ends with `|` or `+`.
