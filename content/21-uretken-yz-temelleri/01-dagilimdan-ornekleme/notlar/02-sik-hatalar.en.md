| Mistake | What happens | Instead |
|---|---|---|
| Leaving out `side="right"` | If `u` lands exactly on a boundary (e.g. 0.45) the wrong category is picked | `np.searchsorted(cum, u, side="right")` |
| The probabilities do not sum to 1 | The last category is picked too often or too rarely; `rng.choice` raises an error | First `p = p / p.sum()` |
| Mixing up `np.log(u)` and `np.log(1 - u)` | Both work, but if `u` is exactly 0, `log(0)` is infinite | `-np.log(1 - u)` (`u` cannot be 1) |
| The rectangle is lower than the curve | The region at the peak is cut off and the distribution is distorted | The height is at least the curve's largest value |
| Changing the order of calls on the same generator | The results come out as different numbers | Keep the order fixed and write it down |
| Deciding from a single draw | Luck misleads | Look at the share over many samples |
| Trusting a tail share with little data | 17 fish gave 6%, the truth was 7.9% | Report the sample count too |
| Taking Monte Carlo as exact | If the model is wrong, so is the result | Compare the assumption with the data |
