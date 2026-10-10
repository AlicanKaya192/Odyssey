`split_bill(total, n)` splits the amount between `n` people and returns each
share as text in a list; but once the shares are rounded to cents the total
does not match (`100.00` three ways → `33.33` three times). Round the shares
**down** (`ROUND_DOWN`) and add the leftover cents one by one to the **first**
shares. The shares must always add up to `total`.

**Expected output:**

```
['33.34', '33.33', '33.33']
['0.02', '0.02', '0.01']
```
