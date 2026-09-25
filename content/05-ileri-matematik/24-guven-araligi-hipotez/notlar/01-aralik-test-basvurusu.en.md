A short version of everything in the lesson. Come back here when you get stuck on a question.

## Confidence intervals

| What | Formula |
|---|---|
| mean ($\sigma$ known) | $\bar{x} \pm z^{*} \frac{\sigma}{\sqrt{n}}$ |
| mean (small $n$, $\sigma$ unknown) | $\bar{x} \pm t^{*} \frac{s}{\sqrt{n}}$ |
| proportion | $\hat{p} \pm z^{*} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$ |
| sample size needed | $n \geq \left(\frac{z^{*}\sigma}{E}\right)^2$, round up |

## Critical values

| Confidence level | $z^{*}$ | two-sided $\alpha$ |
|---|---|---|
| $90$ percent | $1.645$ | $0.10$ |
| $95$ percent | $1.96$ | $0.05$ |
| $99$ percent | $2.576$ | $0.01$ |

## Steps of a hypothesis test

1. Write $H_0$ and $H_1$; choose one- or two-sided and $\alpha$ in advance.
2. Test statistic: $z = \frac{\text{observed} - \text{value in } H_0}{\text{SE}}$.
3. p-value: $2 \cdot P(Z \geq |z|)$ when two-sided, one tail when one-sided.
4. If $p < \alpha$, $H_0$ is rejected; otherwise it is not rejected.

## Errors

| | $H_0$ true | $H_0$ false |
|---|---|---|
| reject | type I ($\alpha$) | correct |
| do not reject | correct | type II ($\beta$) |

Power $= 1 - \beta$.

## Practical tips

- Two independent groups: $\text{SE}_{\text{diff}} = \sqrt{\text{SE}_1^2 + \text{SE}_2^2}$.
- If the confidence interval leaves out $\mu_0$, the test rejects.
- With $m$ tests the Bonferroni threshold is $\frac{\alpha}{m}$.
- "Not rejected" ≠ "$H_0$ is true".
