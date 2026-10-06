The values of two variables are in the wrong places:

```python
left = "pear"
right = "apple"
```

Swap them: in the end `left` should hold `"apple"` and `right` should hold
`"pear"`. Then print both:

```
apple pear
```

Rule: do **not** type the texts `"apple"` and `"pear"` again. Move the
values between the variables.

> Watch out: the most common mistake is writing `left = right` and then
> `right = left`. Both end up holding the same value, because the first
> line wiped out the old value of `left`. You need to keep the old value
> somewhere.
