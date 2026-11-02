`stride_property(letter)` should return the English name of the security
property a STRIDE letter breaks:

- `S` → `"authenticity"`, `T` → `"integrity"`, `R` → `"non-repudiation"`,
- `I` → `"confidentiality"`, `D` → `"availability"`, `E` → `"authorization"`.

The letter may come in lower case. `None` for an unknown letter.

**Expected output:**

```
S authenticity
t integrity
I confidentiality
e authorization
X None
```
