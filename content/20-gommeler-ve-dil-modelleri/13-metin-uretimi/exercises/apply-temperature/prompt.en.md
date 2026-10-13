`apply_temperature(probs, t)` should reweight a word → probability dictionary
with temperature: turn each probability into `p ** (1 / t)`, then divide so
they sum to 1. 3 places, keeping the order of the words.

**Expected output:**

```
0.5 order=0.783 parcel=0.196 box=0.022
1.0 order=0.6 parcel=0.3 box=0.1
2.0 order=0.473 parcel=0.334 box=0.193
```
