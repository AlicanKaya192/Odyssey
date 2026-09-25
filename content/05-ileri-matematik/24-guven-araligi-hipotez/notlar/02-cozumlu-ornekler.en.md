A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. A confidence interval for the mean

**Question:** $n = 49$, $\bar{x} = 120$, $\sigma = 14$. What is the $95$
percent confidence interval?

$\text{SE} = \frac{14}{7} = 2$; margin of error $1.96 \cdot 2 = 3.92$. The
interval is $[116.08, \ 123.92]$.

## 2. A different confidence level

**Question:** With the same data, what is the $99$ percent confidence
interval?

$2.576 \cdot 2 = 5.152$; the interval is $[114.85, \ 125.15]$. Wider.

## 3. The sample size needed

**Question:** $\sigma = 12$; the margin of error should be at most $2$ at
$95$ percent confidence. How many observations?

$\left(\frac{1.96 \cdot 12}{2}\right)^2 = 11.76^2 = 138.3$; round up:
$139$.

## 4. An interval for a proportion

**Question:** $120$ of $400$ people said "yes". What is the $95$ percent
confidence interval?

$\hat{p} = 0.3$; $\text{SE} = \sqrt{\frac{0.3 \cdot 0.7}{400}} \approx
0.0229$; margin of error $\approx 0.045$. The interval is about
$[0.255, \ 0.345]$.

## 5. A two-sided test

**Question:** $H_0: \mu = 80$, $\sigma = 10$, $n = 25$, $\bar{x} = 83.5$.
What is the decision with $\alpha = 0.05$?

$\text{SE} = 2$, $z = 1.75$. $P(Z \geq 1.75) \approx 0.040$; the two-sided
p $\approx 0.080 > 0.05$: $H_0$ is not rejected.

## 6. A one-sided test

**Question:** With the same data, what if $H_1: \mu > 80$ had been chosen
before looking at the data?

One tail: p $\approx 0.040 < 0.05$: rejected. If the direction was not
chosen in advance, this calculation is invalid.

## 7. An interval and a test

**Question:** The $95$ percent confidence interval is $[4.1, \ 7.3]$. What
does a two-sided test of $H_0: \mu = 4$ with $\alpha = 0.05$ say?

$4$ is outside the interval: $H_0$ is rejected.

## 8. The difference of two proportions

**Question:** In group A $150$ of $1000$ people clicked, in group B $180$ of
$1000$. What are the standard error of the difference and $z$?

$\text{SE}_{\text{diff}} = \sqrt{\frac{0.15 \cdot 0.85}{1000} +
\frac{0.18 \cdot 0.82}{1000}} = \sqrt{0.0002751} \approx 0.0166$;
$z = \frac{0.03}{0.0166} \approx 1.81$. Two-sided p $\approx 0.07$: not
significant at the 5 percent level.

## 9. Multiple comparisons

**Question:** $10$ independent tests, $H_0$ true in all, $\alpha = 0.05$.
What is the probability of at least one false alarm? The Bonferroni
threshold?

$1 - 0.95^{10} \approx 0.40$. The threshold is $\frac{0.05}{10} = 0.005$.

## 10. Kinds of error

**Question:** In a spam filter $H_0$ is "the email is normal". An important
work email landing in spam is which kind of error?

$H_0$ was true and was rejected: a type I error.
