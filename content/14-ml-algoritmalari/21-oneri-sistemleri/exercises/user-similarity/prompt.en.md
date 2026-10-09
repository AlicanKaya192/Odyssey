Write the function `user_similarity(a, b)` (`0` means no rating): from
each user's filled ratings subtract their own mean, leave empty ones at 0;
return the cosine similarity of the two deviation vectors,
`round(..., 3)`. If either vector is zero, 0.

**Expected output:**

```
1.0
-0.721
```
