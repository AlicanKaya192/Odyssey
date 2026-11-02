If the calculation says "this test takes six months", starting it anyway to
"see what happens" is the worst option: as we saw in the Power Analysis
section, a result that comes out significant at low power exaggerates the
effect. Instead:

## Options

| Way | What changes | Cost |
|---|---|---|
| Aim for a larger effect | MDE grows, n shrinks | We miss small but real improvements |
| A more sensitive metric | the coefficient of variation shrinks | The metric may be further from the real goal |
| Capping extremes | revenue's deviation shrinks | The effect of huge orders is hidden |
| Variance reduction (CUPED) | noise drops using pre-period data | Extra calculation, past data needed |
| More traffic | n fills quickly | Other experiments wait |
| Longer duration | n fills | The decision is late, the audience may change |

## Don't

- Start a low-power test and accept it if it comes out significant.
- Extend the duration while the test runs "to wait a bit longer": the
  duration is written in advance (The Peeking Trap and Sequential Testing
  section).
- Write the base rate from a guess; it is measured from past data.
