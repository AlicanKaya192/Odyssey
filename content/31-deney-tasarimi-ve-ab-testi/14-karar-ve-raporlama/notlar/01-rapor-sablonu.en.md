## Writing the result in one line

```python
def report(rate_a, rate_b, low, high, decision):
    diff = (rate_b - rate_a) * 100
    return (f"A {rate_a:.2%} -> B {rate_b:.2%}: {diff:+.2f} pts "
            f"(95% CI {low * 100:.2f} to {high * 100:.2f}); {decision}")


print(report(0.1199, 0.1376, 0.0101, 0.0253, "ship"))
```

```text
A 11.99% -> B 13.76%: +1.77 pts (95% CI 1.01 to 2.53); ship
```

Both rates, the absolute difference, the interval and the decision in one
line. If a relative difference ("a 15% rise") is written, it goes **next
to** the absolute difference, not instead of it.

## A one-page report

| Part | Content |
|---|---|
| Question | what changed, which primary metric, which practical threshold |
| Plan | sample size, duration, decision rule (as before the test) |
| Trust | SRM p, A/A result, balance |
| Result | both rates, the difference, the 95% interval, p |
| Guardrails | refunds, errors, speed: any breakage |
| Decision | launch / harmful / inconclusive / not worth it, and why |
| Limits | duration, novelty effect, segments, interference |

## The sentences of the four decisions

- **Launch:** "B raises buying by at least the threshold."
- **Harmful:** "B lowers buying; it is not launched."
- **Inconclusive:** "We could not measure the effect with this test; the
  interval is −x to +y."
- **Not worth it:** "The effect is most likely real but below the
  threshold."
