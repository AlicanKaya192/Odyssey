The sensor data with gain is ready. `rule_accuracy(threshold)` should apply
the peak rule to the test windows (`500:600`) (fault if the largest absolute
value exceeds the threshold) and return the accuracy with 2 places.

**Expected output:**

```
0.93
```
