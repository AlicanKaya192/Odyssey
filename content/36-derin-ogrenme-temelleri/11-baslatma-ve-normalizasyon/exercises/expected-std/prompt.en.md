`expected_std(fan_in, nonlinearity)` should compute the standard deviation that the
Kaiming/Xavier family suggests: `gain / sqrt(fan_in)`. The gain comes from
`nn.init.calculate_gain(nonlinearity)`. Return it with 4 places.

**Expected output:**

```
0.0884
0.1667
```
