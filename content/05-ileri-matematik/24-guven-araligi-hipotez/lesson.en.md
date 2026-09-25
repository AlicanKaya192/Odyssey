# Confidence Intervals and Hypothesis Tests

In the previous section the Central Limit Theorem told us how the sample
mean fluctuates around the population mean. Now we turn the question
around: we have a single sample; where is the population mean likely to
be? And when someone says "this drug works" or "the new design brings more
sales", how do we test the claim against data? In this section we will see
**confidence intervals** and **hypothesis tests**; both rest on the same
idea: uncertainty measured by the standard error.

Prerequisites: Probability Distributions; Sampling and the Central Limit
Theorem.

## A point estimate is not enough

Say we found a sample mean $\bar{x} = 52$. The population mean is not
exactly $52$; the question is how far away it could be. Instead of a
single number (a **point estimate**) we give an **interval** that also
shows the uncertainty.

## A confidence interval for the mean

By the CLT, $\bar{X}$ is within $1.96$ standard errors of $\mu$ with
probability $0.95$. Turning this around:

$$
\bar{x} \pm z^{*} \cdot \frac{\sigma}{\sqrt{n}}
$$

- $z^{*}$ is the **critical value**: $1.96$ for $95$ percent, $1.645$ for
  $90$ percent, $2.576$ for $99$ percent.
- The product $z^{*} \cdot \text{SE}$ is called the **margin of error**.

**Example.** $n = 64$, $\bar{x} = 52$, $\sigma = 8$. $\text{SE} = 1$; the
$95$ percent confidence interval is $52 \pm 1.96$, that is
$[50.04, \ 53.96]$.

<figure class="fig">
<svg viewBox="0 0 440 234" width="440"><line class="grid" x1="70.0" y1="170.0" x2="70.0" y2="20.0"/><line class="grid" x1="111.2" y1="170.0" x2="111.2" y2="20.0"/><line class="grid" x1="152.5" y1="170.0" x2="152.5" y2="20.0"/><line class="grid" x1="193.8" y1="170.0" x2="193.8" y2="20.0"/><line class="grid" x1="235.0" y1="170.0" x2="235.0" y2="20.0"/><line class="grid" x1="276.2" y1="170.0" x2="276.2" y2="20.0"/><line class="grid" x1="317.5" y1="170.0" x2="317.5" y2="20.0"/><line class="grid" x1="358.8" y1="170.0" x2="358.8" y2="20.0"/><line class="grid" x1="400.0" y1="170.0" x2="400.0" y2="20.0"/><line class="curve3" stroke-dasharray="5 4" x1="235.0" y1="170.0" x2="235.0" y2="20.0"/><line class="curve" x1="167.1" y1="48.1" x2="302.9" y2="48.1"/><line class="curve" x1="167.1" y1="53.8" x2="167.1" y2="42.5"/><line class="curve" x1="302.9" y1="53.8" x2="302.9" y2="42.5"/><circle class="dot2" cx="235.0" cy="48.1" r="4"/><text class="ink" x="60.0" y="52.1" font-size="12" text-anchor="end">90%</text><text class="dim" x="167.1" y="39.1" font-size="9" text-anchor="middle">50.35</text><text class="dim" x="302.9" y="39.1" font-size="9" text-anchor="middle">53.65</text><line class="curve" x1="154.1" y1="95.0" x2="315.9" y2="95.0"/><line class="curve" x1="154.1" y1="100.6" x2="154.1" y2="89.4"/><line class="curve" x1="315.9" y1="100.6" x2="315.9" y2="89.4"/><circle class="dot2" cx="235.0" cy="95.0" r="4"/><text class="ink" x="60.0" y="99.0" font-size="12" text-anchor="end">95%</text><text class="dim" x="154.1" y="86.0" font-size="9" text-anchor="middle">50.04</text><text class="dim" x="315.9" y="86.0" font-size="9" text-anchor="middle">53.96</text><line class="curve" x1="128.7" y1="141.9" x2="341.3" y2="141.9"/><line class="curve" x1="128.7" y1="147.5" x2="128.7" y2="136.2"/><line class="curve" x1="341.3" y1="147.5" x2="341.3" y2="136.2"/><circle class="dot2" cx="235.0" cy="141.9" r="4"/><text class="ink" x="60.0" y="145.9" font-size="12" text-anchor="end">99%</text><text class="dim" x="128.7" y="132.9" font-size="9" text-anchor="middle">49.42</text><text class="dim" x="341.3" y="132.9" font-size="9" text-anchor="middle">54.58</text><text class="dim" x="70.0" y="184.0" font-size="9" text-anchor="middle">48</text><text class="dim" x="111.2" y="184.0" font-size="9" text-anchor="middle">49</text><text class="dim" x="152.5" y="184.0" font-size="9" text-anchor="middle">50</text><text class="dim" x="193.8" y="184.0" font-size="9" text-anchor="middle">51</text><text class="dim" x="235.0" y="184.0" font-size="9" text-anchor="middle">52</text><text class="dim" x="276.2" y="184.0" font-size="9" text-anchor="middle">53</text><text class="dim" x="317.5" y="184.0" font-size="9" text-anchor="middle">54</text><text class="dim" x="358.8" y="184.0" font-size="9" text-anchor="middle">55</text><text class="dim" x="400.0" y="184.0" font-size="9" text-anchor="middle">56</text><text class="ink" x="235.0" y="200.0" font-size="10" text-anchor="middle">x̄ = 52</text><text class="ink" x="235" y="222" font-size="12" text-anchor="middle">more confidence, a wider interval</text></svg>
  <figcaption>90, 95 and 99 percent confidence intervals for the same sample (x̄ = 52, SE = 1). Being more certain takes a wider interval.</figcaption>
</figure>

**What sets the width?** A higher confidence level makes $z^{*}$ larger and
the interval wider. A larger $n$ makes the standard error smaller and the
interval narrower; halving the margin of error again takes four times the
data.

**The sample size needed.** For a margin of error of at most $E$:

$$
n \geq \left( \frac{z^{*} \sigma}{E} \right)^{2}
$$

If $\sigma = 15$ and $E = 3$ is wanted at $95$ percent confidence,
$n \geq (1.96 \cdot 5)^2 = 96.04$; that is $97$ observations. The result is
always rounded up.

## What does 95 percent mean?

<figure class="fig">
<svg viewBox="0 0 440 334" width="440"><line class="grid" x1="60.0" y1="280.0" x2="60.0" y2="30.0"/><line class="grid" x1="94.0" y1="280.0" x2="94.0" y2="30.0"/><line class="grid" x1="128.0" y1="280.0" x2="128.0" y2="30.0"/><line class="grid" x1="162.0" y1="280.0" x2="162.0" y2="30.0"/><line class="grid" x1="196.0" y1="280.0" x2="196.0" y2="30.0"/><line class="grid" x1="230.0" y1="280.0" x2="230.0" y2="30.0"/><line class="grid" x1="264.0" y1="280.0" x2="264.0" y2="30.0"/><line class="grid" x1="298.0" y1="280.0" x2="298.0" y2="30.0"/><line class="grid" x1="332.0" y1="280.0" x2="332.0" y2="30.0"/><line class="grid" x1="366.0" y1="280.0" x2="366.0" y2="30.0"/><line class="grid" x1="400.0" y1="280.0" x2="400.0" y2="30.0"/><line class="curve" x1="162.0" y1="38.6" x2="295.3" y2="38.6"/><circle class="dot" cx="228.7" cy="38.6" r="3.5"/><line class="curve" x1="133.1" y1="50.8" x2="266.4" y2="50.8"/><circle class="dot" cx="199.7" cy="50.8" r="3.5"/><line class="curve" x1="183.7" y1="63.1" x2="317.0" y2="63.1"/><circle class="dot" cx="250.3" cy="63.1" r="3.5"/><line class="curve" x1="131.6" y1="75.3" x2="264.9" y2="75.3"/><circle class="dot" cx="198.2" cy="75.3" r="3.5"/><line class="curve" x1="220.4" y1="87.6" x2="353.7" y2="87.6"/><circle class="dot" cx="287.0" cy="87.6" r="3.5"/><line class="curve" x1="186.4" y1="99.9" x2="319.7" y2="99.9"/><circle class="dot" cx="253.0" cy="99.9" r="3.5"/><line class="curve" x1="176.5" y1="112.1" x2="309.8" y2="112.1"/><circle class="dot" cx="243.1" cy="112.1" r="3.5"/><line class="curve" x1="178.4" y1="124.4" x2="311.7" y2="124.4"/><circle class="dot" cx="245.0" cy="124.4" r="3.5"/><line class="curve" x1="186.9" y1="136.6" x2="320.2" y2="136.6"/><circle class="dot" cx="253.5" cy="136.6" r="3.5"/><line class="curve" x1="170.6" y1="148.9" x2="303.9" y2="148.9"/><circle class="dot" cx="237.3" cy="148.9" r="3.5"/><line class="curve" x1="219.4" y1="161.1" x2="352.7" y2="161.1"/><circle class="dot" cx="286.1" cy="161.1" r="3.5"/><line class="curve" x1="219.4" y1="173.4" x2="352.7" y2="173.4"/><circle class="dot" cx="286.0" cy="173.4" r="3.5"/><line class="curve" x1="138.3" y1="185.6" x2="271.6" y2="185.6"/><circle class="dot" cx="204.9" cy="185.6" r="3.5"/><line class="curve" x1="201.1" y1="197.9" x2="334.4" y2="197.9"/><circle class="dot" cx="267.7" cy="197.9" r="3.5"/><line class="curve" x1="129.6" y1="210.1" x2="262.8" y2="210.1"/><circle class="dot" cx="196.2" cy="210.1" r="3.5"/><line class="curve2" x1="69.3" y1="222.4" x2="202.6" y2="222.4"/><circle class="dot2" cx="135.9" cy="222.4" r="3.5"/><line class="curve" x1="141.6" y1="234.7" x2="274.8" y2="234.7"/><circle class="dot" cx="208.2" cy="234.7" r="3.5"/><line class="curve" x1="115.3" y1="246.9" x2="248.5" y2="246.9"/><circle class="dot" cx="181.9" cy="246.9" r="3.5"/><line class="curve" x1="148.7" y1="259.2" x2="282.0" y2="259.2"/><circle class="dot" cx="215.3" cy="259.2" r="3.5"/><line class="curve" x1="167.6" y1="271.4" x2="300.9" y2="271.4"/><circle class="dot" cx="234.3" cy="271.4" r="3.5"/><line class="curve3" stroke-dasharray="5 4" x1="230.0" y1="280.0" x2="230.0" y2="30.0"/><text class="ink" x="230.0" y="20.0" font-size="11" text-anchor="middle">true μ = 50</text><text class="dim" x="60.0" y="294.0" font-size="9" text-anchor="middle">40</text><text class="dim" x="94.0" y="294.0" font-size="9" text-anchor="middle">42</text><text class="dim" x="128.0" y="294.0" font-size="9" text-anchor="middle">44</text><text class="dim" x="162.0" y="294.0" font-size="9" text-anchor="middle">46</text><text class="dim" x="196.0" y="294.0" font-size="9" text-anchor="middle">48</text><text class="dim" x="230.0" y="294.0" font-size="9" text-anchor="middle">50</text><text class="dim" x="264.0" y="294.0" font-size="9" text-anchor="middle">52</text><text class="dim" x="298.0" y="294.0" font-size="9" text-anchor="middle">54</text><text class="dim" x="332.0" y="294.0" font-size="9" text-anchor="middle">56</text><text class="dim" x="366.0" y="294.0" font-size="9" text-anchor="middle">58</text><text class="dim" x="400.0" y="294.0" font-size="9" text-anchor="middle">60</text><text class="dim" x="48" y="155" font-size="10" text-anchor="end">sample</text><text class="dim" x="48" y="169" font-size="10" text-anchor="end">1 → 20</text><line class="curve" x1="90" y1="318" x2="118" y2="318"/><circle class="dot" cx="104" cy="318" r="3.5"/><text class="ink" x="126" y="322" font-size="10" text-anchor="start">interval containing μ</text><line class="curve2" x1="260" y1="318" x2="288" y2="318"/><circle class="dot2" cx="274" cy="318" r="3.5"/><text class="ink" x="296" y="322" font-size="10" text-anchor="start">interval missing μ</text></svg>
  <figcaption>20 separate samples were drawn from the same population (μ = 50) and a 95 percent confidence interval computed from each. The intervals move with the sample; this time 19 of the 20 contain μ and one misses it.</figcaption>
</figure>

$\mu$ is a fixed, unknown number; it is the interval that is random. "95
percent confidence" is about the **method**: if we compute intervals from
a hundred samples this way, about $95$ of them contain $\mu$. The single
interval we have either contains it or does not; we do not know which.

## Unknown σ and small samples

$\sigma$ is usually unknown; the sample standard deviation $s$ is used in
its place. For large $n$ ($n \geq 30$) the result barely changes. In small
samples $s$ is itself uncertain, so a slightly larger $t^{*}$ value (from
Student's $t$ distribution, with $n - 1$ degrees of freedom) is used
instead of $z^{*}$. For example, for $n = 16$ at $95$ percent
$t^{*} = 2.131$; larger than $1.96$, so the interval is a little wider.

## A confidence interval for a proportion

For yes–no data:

$$
\hat{p} \pm z^{*} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}
$$

**Example.** In a survey of $1000$ people, $\hat{p} = 0.52$.
$\text{SE} = \sqrt{\frac{0.52 \cdot 0.48}{1000}} \approx 0.0158$; the margin
of error is $1.96 \cdot 0.0158 \approx 0.031$. The interval is about
$[0.489, \ 0.551]$. $0.5$ is inside it: we cannot say a majority said
"yes".

## Hypothesis tests

To test a claim with data, two hypotheses are written:

- The **null hypothesis** $H_0$: "no difference", "no effect". For example
  $\mu = 500$.
- The **alternative hypothesis** $H_1$: what we are looking for. For
  example $\mu \neq 500$.

The logic resembles a proof by contradiction: assume $H_0$ is true, then
see how surprising the observed data is under that assumption.

**The test statistic.** How many standard errors the observed mean is from
the value in $H_0$:

$$
z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}
$$

**The p-value.** If $H_0$ is true, the probability of seeing a result at
least as extreme as the one observed. A small p-value says the data does
not fit $H_0$ well.

**Example.** A factory says it fills bottles with $500$ ml on average;
$\sigma = 6$ ml. The mean of $36$ bottles is $497.8$ ml. $\text{SE} = 1$,
$z = -2.2$. The two-sided p-value is
$2 \cdot P(Z \leq -2.2) = 2 \cdot 0.014 = 0.028$.

<figure class="fig">
<svg viewBox="0 0 440 250" width="440"><line class="grid" x1="30.0" y1="200.0" x2="30.0" y2="30.0"/><line class="grid" x1="77.5" y1="200.0" x2="77.5" y2="30.0"/><line class="grid" x1="125.0" y1="200.0" x2="125.0" y2="30.0"/><line class="grid" x1="172.5" y1="200.0" x2="172.5" y2="30.0"/><line class="grid" x1="220.0" y1="200.0" x2="220.0" y2="30.0"/><line class="grid" x1="267.5" y1="200.0" x2="267.5" y2="30.0"/><line class="grid" x1="315.0" y1="200.0" x2="315.0" y2="30.0"/><line class="grid" x1="362.5" y1="200.0" x2="362.5" y2="30.0"/><line class="grid" x1="410.0" y1="200.0" x2="410.0" y2="30.0"/><line class="grid" x1="30.0" y1="200.0" x2="410.0" y2="200.0"/><line class="line" x1="30.0" y1="200.0" x2="410.0" y2="200.0"/><polygon class="dot2" opacity="0.55" points="30.0,200.0 30.0,199.9 30.7,199.9 31.4,199.9 32.1,199.9 32.9,199.9 33.6,199.9 34.3,199.9 35.0,199.9 35.7,199.9 36.4,199.9 37.1,199.9 37.8,199.9 38.6,199.9 39.3,199.9 40.0,199.9 40.7,199.9 41.4,199.9 42.1,199.9 42.8,199.9 43.5,199.8 44.2,199.8 45.0,199.8 45.7,199.8 46.4,199.8 47.1,199.8 47.8,199.8 48.5,199.8 49.2,199.8 49.9,199.7 50.7,199.7 51.4,199.7 52.1,199.7 52.8,199.7 53.5,199.7 54.2,199.7 54.9,199.6 55.7,199.6 56.4,199.6 57.1,199.6 57.8,199.5 58.5,199.5 59.2,199.5 59.9,199.5 60.6,199.4 61.4,199.4 62.1,199.4 62.8,199.4 63.5,199.3 64.2,199.3 64.9,199.3 65.6,199.2 66.3,199.2 67.0,199.1 67.8,199.1 68.5,199.0 69.2,199.0 69.9,199.0 70.6,198.9 71.3,198.9 72.0,198.8 72.8,198.7 73.5,198.7 74.2,198.6 74.9,198.6 75.6,198.5 76.3,198.4 77.0,198.3 77.7,198.3 78.5,198.2 79.2,198.1 79.9,198.0 80.6,197.9 81.3,197.8 82.0,197.7 82.7,197.6 83.4,197.5 84.1,197.4 84.9,197.3 85.6,197.2 86.3,197.1 87.0,196.9 87.7,196.8 88.4,196.7 89.1,196.5 89.8,196.4 90.6,196.2 91.3,196.1 92.0,195.9 92.7,195.8 93.4,195.6 94.1,195.4 94.8,195.2 95.5,195.0 96.3,194.8 97.0,194.6 97.7,194.4 98.4,194.2 99.1,194.0 99.8,193.7 100.5,193.5 101.2,193.2 102.0,193.0 102.7,192.7 103.4,192.4 104.1,192.1 104.8,191.9 105.5,191.6 106.2,191.2 107.0,190.9 107.7,190.6 108.4,190.3 109.1,189.9 109.8,189.5 110.5,189.2 111.2,188.8 111.9,188.4 112.6,188.0 113.4,187.6 114.1,187.2 114.8,186.7 115.5,186.3 115.5,200.0"/><polygon class="dot2" opacity="0.55" points="324.5,200.0 324.5,186.3 325.2,186.7 325.9,187.2 326.6,187.6 327.3,188.0 328.1,188.4 328.8,188.8 329.5,189.2 330.2,189.5 330.9,189.9 331.6,190.3 332.3,190.6 333.1,190.9 333.8,191.2 334.5,191.6 335.2,191.9 335.9,192.1 336.6,192.4 337.3,192.7 338.0,193.0 338.8,193.2 339.5,193.5 340.2,193.7 340.9,194.0 341.6,194.2 342.3,194.4 343.0,194.6 343.7,194.8 344.4,195.0 345.2,195.2 345.9,195.4 346.6,195.6 347.3,195.8 348.0,195.9 348.7,196.1 349.4,196.2 350.2,196.4 350.9,196.5 351.6,196.7 352.3,196.8 353.0,196.9 353.7,197.1 354.4,197.2 355.1,197.3 355.9,197.4 356.6,197.5 357.3,197.6 358.0,197.7 358.7,197.8 359.4,197.9 360.1,198.0 360.8,198.1 361.6,198.2 362.3,198.3 363.0,198.3 363.7,198.4 364.4,198.5 365.1,198.6 365.8,198.6 366.5,198.7 367.2,198.7 368.0,198.8 368.7,198.9 369.4,198.9 370.1,199.0 370.8,199.0 371.5,199.0 372.2,199.1 373.0,199.1 373.7,199.2 374.4,199.2 375.1,199.3 375.8,199.3 376.5,199.3 377.2,199.4 377.9,199.4 378.6,199.4 379.4,199.4 380.1,199.5 380.8,199.5 381.5,199.5 382.2,199.5 382.9,199.6 383.6,199.6 384.4,199.6 385.1,199.6 385.8,199.7 386.5,199.7 387.2,199.7 387.9,199.7 388.6,199.7 389.3,199.7 390.1,199.7 390.8,199.8 391.5,199.8 392.2,199.8 392.9,199.8 393.6,199.8 394.3,199.8 395.0,199.8 395.8,199.8 396.5,199.8 397.2,199.9 397.9,199.9 398.6,199.9 399.3,199.9 400.0,199.9 400.7,199.9 401.4,199.9 402.2,199.9 402.9,199.9 403.6,199.9 404.3,199.9 405.0,199.9 405.7,199.9 406.4,199.9 407.1,199.9 407.9,199.9 408.6,199.9 409.3,199.9 410.0,199.9 410.0,200.0"/><polyline class="curve" fill="none" points="30.0,199.9 31.6,199.9 33.2,199.9 34.8,199.9 36.3,199.9 37.9,199.9 39.5,199.9 41.1,199.9 42.7,199.9 44.2,199.8 45.8,199.8 47.4,199.8 49.0,199.8 50.6,199.7 52.2,199.7 53.8,199.7 55.3,199.6 56.9,199.6 58.5,199.5 60.1,199.5 61.7,199.4 63.3,199.3 64.8,199.3 66.4,199.2 68.0,199.1 69.6,199.0 71.2,198.9 72.8,198.7 74.3,198.6 75.9,198.5 77.5,198.3 79.1,198.1 80.7,197.9 82.2,197.7 83.8,197.5 85.4,197.2 87.0,196.9 88.6,196.6 90.2,196.3 91.8,196.0 93.3,195.6 94.9,195.2 96.5,194.8 98.1,194.3 99.7,193.8 101.2,193.2 102.8,192.6 104.4,192.0 106.0,191.3 107.6,190.6 109.2,189.9 110.8,189.1 112.3,188.2 113.9,187.3 115.5,186.3 117.1,185.3 118.7,184.2 120.2,183.0 121.8,181.8 123.4,180.5 125.0,179.1 126.6,177.7 128.2,176.2 129.8,174.6 131.3,173.0 132.9,171.3 134.5,169.5 136.1,167.6 137.7,165.7 139.2,163.7 140.8,161.6 142.4,159.4 144.0,157.1 145.6,154.8 147.2,152.4 148.8,150.0 150.3,147.4 151.9,144.8 153.5,142.2 155.1,139.4 156.7,136.6 158.2,133.8 159.8,130.9 161.4,128.0 163.0,125.0 164.6,122.0 166.2,118.9 167.8,115.8 169.3,112.7 170.9,109.6 172.5,106.5 174.1,103.4 175.7,100.3 177.2,97.2 178.8,94.1 180.4,91.1 182.0,88.1 183.6,85.1 185.2,82.2 186.8,79.4 188.3,76.6 189.9,73.9 191.5,71.3 193.1,68.7 194.7,66.3 196.2,64.0 197.8,61.8 199.4,59.7 201.0,57.7 202.6,55.9 204.2,54.2 205.8,52.6 207.3,51.2 208.9,50.0 210.5,48.9 212.1,48.0 213.7,47.2 215.2,46.6 216.8,46.2 218.4,45.9 220.0,45.9 221.6,45.9 223.2,46.2 224.7,46.6 226.3,47.2 227.9,48.0 229.5,48.9 231.1,50.0 232.7,51.2 234.2,52.6 235.8,54.2 237.4,55.9 239.0,57.7 240.6,59.7 242.2,61.8 243.8,64.0 245.3,66.3 246.9,68.7 248.5,71.3 250.1,73.9 251.7,76.6 253.2,79.4 254.8,82.2 256.4,85.1 258.0,88.1 259.6,91.1 261.2,94.1 262.8,97.2 264.3,100.3 265.9,103.4 267.5,106.5 269.1,109.6 270.7,112.7 272.2,115.8 273.8,118.9 275.4,122.0 277.0,125.0 278.6,128.0 280.2,130.9 281.8,133.8 283.3,136.6 284.9,139.4 286.5,142.2 288.1,144.8 289.7,147.4 291.2,150.0 292.8,152.4 294.4,154.8 296.0,157.1 297.6,159.4 299.2,161.6 300.8,163.7 302.3,165.7 303.9,167.6 305.5,169.5 307.1,171.3 308.7,173.0 310.2,174.6 311.8,176.2 313.4,177.7 315.0,179.1 316.6,180.5 318.2,181.8 319.8,183.0 321.3,184.2 322.9,185.3 324.5,186.3 326.1,187.3 327.7,188.2 329.2,189.1 330.8,189.9 332.4,190.6 334.0,191.3 335.6,192.0 337.2,192.6 338.8,193.2 340.3,193.8 341.9,194.3 343.5,194.8 345.1,195.2 346.7,195.6 348.2,196.0 349.8,196.3 351.4,196.6 353.0,196.9 354.6,197.2 356.2,197.5 357.8,197.7 359.3,197.9 360.9,198.1 362.5,198.3 364.1,198.5 365.7,198.6 367.2,198.7 368.8,198.9 370.4,199.0 372.0,199.1 373.6,199.2 375.2,199.3 376.8,199.3 378.3,199.4 379.9,199.5 381.5,199.5 383.1,199.6 384.7,199.6 386.2,199.7 387.8,199.7 389.4,199.7 391.0,199.8 392.6,199.8 394.2,199.8 395.8,199.8 397.3,199.9 398.9,199.9 400.5,199.9 402.1,199.9 403.7,199.9 405.2,199.9 406.8,199.9 408.4,199.9 410.0,199.9"/><line class="curve3" stroke-dasharray="5 4" x1="126.9" y1="200.0" x2="126.9" y2="84.1"/><line class="curve3" stroke-dasharray="5 4" x1="313.1" y1="200.0" x2="313.1" y2="84.1"/><text class="dim" x="126.9" y="66.1" font-size="10" text-anchor="middle">critical value</text><text class="dim" x="126.9" y="79.1" font-size="10" text-anchor="middle">−1.96</text><text class="dim" x="313.1" y="66.1" font-size="10" text-anchor="middle">critical value</text><text class="dim" x="313.1" y="79.1" font-size="10" text-anchor="middle">1.96</text><circle class="dot2" cx="115.5" cy="200.0" r="4"/><text class="ink" x="115.5" y="236.0" font-size="10" text-anchor="middle">observed z = −2.2</text><text class="ink" x="72.8" y="176.8" font-size="10" text-anchor="middle">each tail 0.014</text><text class="ink" x="367.2" y="176.8" font-size="10" text-anchor="middle">each tail 0.014</text><text class="ink" x="220.0" y="122.7" font-size="12" text-anchor="middle">p = 0.028</text><text class="dim" x="220.0" y="22.0" font-size="10" text-anchor="middle">distribution of Z if H₀ holds</text><text class="dim" x="77.5" y="214.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="125.0" y="214.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="172.5" y="214.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="220.0" y="214.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="267.5" y="214.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="315.0" y="214.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="362.5" y="214.0" font-size="9" text-anchor="middle">3</text></svg>
  <figcaption>If H₀ holds, z is standard normal. The probability of results more extreme than the observed z = −2.2 is the sum of the two tails: p = 0.028. The dashed lines are the critical values ±1.96 at the 5 percent level.</figcaption>
</figure>

**The decision.** A **significance level** $\alpha$ is chosen in advance
(usually $0.05$). If $p < \alpha$, $H_0$ is **rejected**; otherwise it is
**not rejected**. In the example $0.028 < 0.05$: the bottles seem to be
filled less than claimed. Had $\alpha = 0.01$ been chosen, it would not be
rejected.

**One-sided and two-sided.** $H_1: \mu \neq \mu_0$ is two-sided; both tails
count. $H_1: \mu < \mu_0$ is one-sided; only one tail counts and the
p-value halves. The direction must be chosen before looking at the data.

## Two kinds of error

| | $H_0$ actually true | $H_0$ actually false |
|---|---|---|
| $H_0$ rejected | **type I error** (probability $\alpha$) | correct decision |
| $H_0$ not rejected | correct decision | **type II error** (probability $\beta$) |

- Type I error: counting an effect that is not there (a false alarm).
- Type II error: missing an effect that is there.
- $1 - \beta$ is the test's **power**: the probability of catching a real
  effect. Power grows with $n$ and with the size of the effect.

Lowering $\alpha$ reduces type I errors but increases type II errors; the
way to reduce both is more data.

## An interval and a test are two sides of one coin

If the $95$ percent confidence interval does not contain $\mu_0$, a
two-sided test with $\alpha = 0.05$ rejects $H_0: \mu = \mu_0$; if it does,
the test does not reject. The interval gives more information: it answers
not only "is there a difference" but also "how large could it be".

## Comparing two groups

The standard error of the difference between the means (or proportions) of
two independent groups is the square root of the sum of the squared
standard errors:

$$
\text{SE}_{\text{diff}} = \sqrt{\text{SE}_1^2 + \text{SE}_2^2}
$$

The test statistic is $z = \frac{\text{difference}}{\text{SE}_{\text{diff}}}$.

## In machine learning

**A/B tests.** A site's old design brought purchases from $10$ percent of
$2000$ visitors, the new one from $12$ percent of $2000$.
$\text{SE}_{\text{diff}} = \sqrt{\frac{0.1 \cdot 0.9}{2000} +
\frac{0.12 \cdot 0.88}{2000}} \approx 0.0099$; $z \approx 2.02$,
p $\approx 0.043$. Significant at the 5 percent level, but only just.

**Model comparison.** The difference in test accuracy between two models is
also a two-group comparison; if they are compared on the same test set,
paired tests that match example by example are more powerful.

**Multiple comparisons.** If we try $20$ settings none of which has a real
effect, with $\alpha = 0.05$ the probability that at least one comes out
"significant" is $1 - 0.95^{20} \approx 0.64$. Trying many things and
reporting only the significant one (**p-hacking**) produces false results.
A simple safeguard is the **Bonferroni** correction: for $m$ tests the
threshold is $\frac{\alpha}{m}$.

**Statistical and practical significance.** With a very large sample even a
$0.01$ percent difference comes out significant; it may still be too small
to matter. A confidence interval lets us see the size of the effect.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>the p-value is the probability that H₀ is true</p>
      <p>not rejected, so H₀ is true</p>
      <p>significant, so important</p>
      <p>switching to a one-sided test after seeing the data</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>the p-value is the probability of data this extreme if H₀ is true</p>
      <p>not rejected: the data was not enough, H₀ is not proven</p>
      <p>look at the size of the effect with a confidence interval</p>
      <p>choose the hypotheses and α before the data</p>
    </div>
  </div>
  <figcaption>The p-value is a probability about the data, not about the hypothesis.</figcaption>
</figure>

- **"μ is in this interval with probability 95 percent."** $\mu$ is not
  random; 95 percent is the method's long-run hit rate.
- **Confusing the standard deviation with the standard error.** The
  interval is $\bar{x} \pm 1.96 \, \frac{\sigma}{\sqrt{n}}$, not
  $\bar{x} \pm 1.96 \, \sigma$.

## Summary

- Confidence interval: $\bar{x} \pm z^{*} \frac{\sigma}{\sqrt{n}}$; for a
  proportion $\hat{p} \pm z^{*} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$.
- $z^{*}$: $1.645$ for $90$ percent, $1.96$ for $95$, $2.576$ for $99$. In
  small samples, $t^{*}$.
- Sample size needed: $n \geq \left(\frac{z^{*}\sigma}{E}\right)^2$.
- Hypothesis test: $z = \frac{\bar{x} - \mu_0}{\text{SE}}$; if the p-value
  is below $\alpha$, $H_0$ is rejected.
- Type I error $\alpha$, type II error $\beta$, power $1 - \beta$.
- Many tests make false alarms likely; the threshold must be corrected.
