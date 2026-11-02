## Measures

| Measure | Calculation | What does it point to? |
|---|---|---|
| Common word count | `the`, `and`… in the decrypted text | The right key in a small key space |
| Letter percentage | `100 * count / total` | The language's fingerprint |
| Chi-squared | Σ (observed − expected)² / expected | Small means the text looks like English |
| Index of coincidence | Σ n(n−1) / (N(N−1)) | English ≈ 0.066, random ≈ 0.038 |

## Which one for which cipher?

- **Caesar:** try all 26 shifts and pick the one with the smallest
  chi-squared.
- **Substitution:** sort the letters by frequency, match them with
  `etaoin…`, then fix with word patterns (`the`, `a`, double letters).
- **Vigenère:** try lengths starting from 1; the first length whose average
  column IoC passes 0.06 is the key length. Then each column is a Caesar.
- **Transposition:** if the letter percentages match English, the cipher is
  a transposition; try row counts.

## Python patterns

- Letters only: `[c for c in text.lower() if c.isalpha()]`.
- Counting: `Counter(letters).most_common(n)`.
- Every `L`-th letter: `letters[i::L]`.
- Picking the smaller one on a tie: sort `(score, shift)` tuples.

## To remember

Statistics are shaky on short text: with a few dozen letters chi-squared
can be wrong, with a few hundred it almost never is.
