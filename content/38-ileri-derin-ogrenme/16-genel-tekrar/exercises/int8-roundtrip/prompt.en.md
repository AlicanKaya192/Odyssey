`int8_roundtrip(values)` should compress the values with symmetric `int8`
quantisation (scale `largest |w| / 127`), restore them with the scale and
return a list with 3 places.

**Expected output:**

```
[1.27, -0.5, 0.0]
```
