In `price2` the price per square metre changes with the city.
`interaction_slope(city)` should add the **interaction** to the formula
(`area * C(city)`) and return the `area:C(city)[T.<city>]` coefficient with 2
places. The starter code writes `+`; with no interaction coefficient it
fails.

**Expected output:**

```
1.49
-0.02
```
