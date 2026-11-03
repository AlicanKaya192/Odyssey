The capstone analysis is a template. To try it with your own data, fill in
the plan below, then apply the steps in order.

## Plan template

| Field | Your answer |
|---|---|
| Change | ... |
| Hypothesis | "... will rise because of ..." |
| Primary metric and its unit | ... (per user or per view?) |
| Practical threshold | ... points |
| Guardrail metrics | ... (with their limits) |
| Covariate (CUPED) | ... (measured before the test) |
| Segments | one or two at most |
| Sample and duration | ... users, ... days |
| Looking rule | only the last day / sequential thresholds |
| Decision rule | the four outcomes and what to do in each |

## If there is no data

Build your own scenario with the functions in `ab_data.py`: give
`make_capstone` a different `lift` (e.g. 0 or −0.05) and see how the same
analysis reaches other results. As someone who knows the true effect,
check whether the analysis finds it: this is the best way to test the
method.

## Common mistakes

- Writing the plan after the test.
- Changing the primary metric according to the result.
- Reporting an inconclusive result as "no effect".
- Highlighting the most striking segment.
