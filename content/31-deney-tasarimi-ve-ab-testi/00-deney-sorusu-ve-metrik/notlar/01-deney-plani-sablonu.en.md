Filled in before the test starts and not changed afterwards. If it must
change, a dated note with the reason is added.

| Heading | Example |
|---|---|
| Change | The checkout button moves to the top of the page |
| Reason | On mobile the button is not on the first screen |
| Primary metric | Per-user buying rate (`bought`) |
| Expected direction | Increase |
| Minimum detectable effect | +0.5 points |
| Guardrail metrics | Refund rate (among buyers), page load time |
| Unit of assignment | User |
| Split | 50% / 50% |
| Sample and duration | From a power analysis; at least one full week |
| Test and α | Two-proportion z-test, α = 0.05, two-sided |

## Writing a metric down

A metric is defined by four things:

1. **Numerator:** what is counted? (users who bought)
2. **Denominator:** what is it divided by? (users who entered the test)
3. **Window:** over what period? (14 days after assignment)
4. **Filter:** who is included? (only those who reached the checkout page)

Saying "conversion rate" is not enough; if these four are not written, two
people compute two different numbers under the same name.

## Common mistakes

- Making the "best looking" metric primary after the test.
- Choosing no guardrail metric: refunds can explode while buying rises.
- Making a metric with an unclear direction, like time, the target.
- Mixing up the denominator: "refunds per buyer" and "refunds per user"
  are different numbers.
