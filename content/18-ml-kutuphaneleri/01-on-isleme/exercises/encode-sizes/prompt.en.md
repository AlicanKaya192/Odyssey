`encode_sizes(sizes)` should encode sizes with `OrdinalEncoder` so that **S=0,
M=1, L=2, XL=3** (`categories=[["S", "M", "L", "XL"]]`) and return an `int`
list. The starter code gives no order: it encodes alphabetically.

**Expected output:**

```
[1, 0, 3, 2, 0]
```
