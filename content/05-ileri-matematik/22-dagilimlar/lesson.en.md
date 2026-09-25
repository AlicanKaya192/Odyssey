# Probability Distributions

Some distributions come up so often that they have names. Whether an e-mail
is spam, how many of $100$ visitors buy, how many orders arrive in an hour,
how far a measurement strays from its mean: each is described by a
well-known distribution, and once learned it is used everywhere. Machine
learning is the same: binary classification is Bernoulli, multi-class
classification is the categorical distribution, and mean squared error is
tied to the normal distribution. In this section we will see the most
important discrete distributions (Bernoulli, binomial, Poisson) and
continuous ones (uniform, exponential, normal).

Prerequisites: Random Variables, Expectation and Variance; Counting in
MATH 1.

## The Bernoulli distribution

A single yes–no trial: $1$ ("success") with probability $p$, $0$ with
probability $1 - p$. A coin toss, whether a customer clicks, whether an
e-mail is spam.

$$
E[X] = p \qquad \operatorname{Var}(X) = p(1 - p)
$$

The variance is largest at $p = 0.5$ ($0.25$): where the outcome is most
uncertain. As $p$ approaches $0$ or $1$ the outcome becomes certain and the
variance shrinks.

## The binomial distribution

The number of successes in $n$ independent Bernoulli trials. For $k$
successes, which of the $n$ trials succeed can be chosen in $\binom{n}{k}$
ways, and each way has probability $p^k (1 - p)^{n - k}$:

$$
P(X = k) = \binom{n}{k} p^k (1 - p)^{n - k} \qquad E[X] = np \qquad \operatorname{Var}(X) = np(1 - p)
$$

The expected value and variance add up directly, because the count is a
sum of $n$ Bernoullis.

<figure class="fig">
<svg viewBox="0 0 440 256" width="440"><line class="grid" x1="68.8" y1="200.0" x2="68.8" y2="20.0"/><line class="grid" x1="100.0" y1="200.0" x2="100.0" y2="20.0"/><line class="grid" x1="131.2" y1="200.0" x2="131.2" y2="20.0"/><line class="grid" x1="162.5" y1="200.0" x2="162.5" y2="20.0"/><line class="grid" x1="193.8" y1="200.0" x2="193.8" y2="20.0"/><line class="grid" x1="225.0" y1="200.0" x2="225.0" y2="20.0"/><line class="grid" x1="256.2" y1="200.0" x2="256.2" y2="20.0"/><line class="grid" x1="287.5" y1="200.0" x2="287.5" y2="20.0"/><line class="grid" x1="318.8" y1="200.0" x2="318.8" y2="20.0"/><line class="grid" x1="350.0" y1="200.0" x2="350.0" y2="20.0"/><line class="grid" x1="381.2" y1="200.0" x2="381.2" y2="20.0"/><line class="grid" x1="50.0" y1="200.0" x2="400.0" y2="200.0"/><line class="grid" x1="50.0" y1="140.0" x2="400.0" y2="140.0"/><line class="grid" x1="50.0" y1="80.0" x2="400.0" y2="80.0"/><line class="grid" x1="50.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="50.0" y1="200.0" x2="400.0" y2="200.0"/><line class="line" x1="68.8" y1="200.0" x2="68.8" y2="20.0"/><text class="dim" x="68.8" y="213.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="100.0" y="213.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="131.2" y="213.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="162.5" y="213.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="193.8" y="213.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="225.0" y="213.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="256.2" y="213.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="287.5" y="213.0" font-size="9" text-anchor="middle">7</text><text class="dim" x="318.8" y="213.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="350.0" y="213.0" font-size="9" text-anchor="middle">9</text><text class="dim" x="381.2" y="213.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="63.8" y="143.0" font-size="9" text-anchor="end">0.1</text><text class="dim" x="63.8" y="83.0" font-size="9" text-anchor="end">0.2</text><rect class="dot" opacity="0.6" x="57.8" y="183.1" width="21.9" height="16.9"/><rect class="dot" opacity="0.6" x="89.1" y="127.4" width="21.8" height="72.6"/><rect class="dot" opacity="0.6" x="120.3" y="59.9" width="21.9" height="140.1"/><rect class="dot" opacity="0.6" x="151.6" y="39.9" width="21.8" height="160.1"/><rect class="dot" opacity="0.6" x="182.8" y="79.9" width="21.9" height="120.1"/><rect class="dot" opacity="0.6" x="214.1" y="138.2" width="21.8" height="61.8"/><rect class="dot" opacity="0.6" x="245.3" y="177.9" width="21.9" height="22.1"/><rect class="dot" opacity="0.6" x="276.6" y="194.6" width="21.8" height="5.4"/><rect class="dot" opacity="0.6" x="307.8" y="199.1" width="21.9" height="0.9"/><rect class="dot" opacity="0.6" x="339.1" y="199.9" width="21.8" height="0.1"/><rect class="dot" opacity="0.6" x="370.3" y="200.0" width="21.9" height="0.0"/><text class="ink" x="162.5" y="34.9" font-size="10" text-anchor="middle">0.267</text><text class="dim" x="400.0" y="228.0" font-size="10" text-anchor="end">number of successes k</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">P(X = k)</text><text class="ink" x="225" y="244" font-size="12" text-anchor="middle">Binom(n = 10, p = 0.3): most likely 3, E[X] = 3</text></svg>
  <figcaption>10 trials with success probability 0.3. The most likely result is 3 successes (0.267); 7 or more is almost impossible. The distribution stretches a little to the right.</figcaption>
</figure>

**Example.** Each person who sees an ad clicks with probability $0.3$; $10$
people see it. Exactly $3$ clicks:
$\binom{10}{3} \cdot 0.3^3 \cdot 0.7^7 = 120 \cdot 0.027 \cdot 0.0824 \approx 0.267$.
Expected clicks $3$, variance $2.1$.

## The Poisson distribution

The number of events that happen **independently** and **at a constant
average rate** in a given time or space: orders in an hour, typos on a
page, requests to a server per minute. If the average is $\lambda$:

$$
P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!} \qquad E[X] = \operatorname{Var}(X) = \lambda
$$

<figure class="fig">
<svg viewBox="0 0 440 246" width="440"><line class="grid" x1="68.8" y1="190.0" x2="68.8" y2="20.0"/><line class="grid" x1="100.0" y1="190.0" x2="100.0" y2="20.0"/><line class="grid" x1="131.2" y1="190.0" x2="131.2" y2="20.0"/><line class="grid" x1="162.5" y1="190.0" x2="162.5" y2="20.0"/><line class="grid" x1="193.8" y1="190.0" x2="193.8" y2="20.0"/><line class="grid" x1="225.0" y1="190.0" x2="225.0" y2="20.0"/><line class="grid" x1="256.2" y1="190.0" x2="256.2" y2="20.0"/><line class="grid" x1="287.5" y1="190.0" x2="287.5" y2="20.0"/><line class="grid" x1="318.8" y1="190.0" x2="318.8" y2="20.0"/><line class="grid" x1="350.0" y1="190.0" x2="350.0" y2="20.0"/><line class="grid" x1="381.2" y1="190.0" x2="381.2" y2="20.0"/><line class="grid" x1="50.0" y1="190.0" x2="400.0" y2="190.0"/><line class="grid" x1="50.0" y1="156.0" x2="400.0" y2="156.0"/><line class="grid" x1="50.0" y1="122.0" x2="400.0" y2="122.0"/><line class="grid" x1="50.0" y1="88.0" x2="400.0" y2="88.0"/><line class="grid" x1="50.0" y1="54.0" x2="400.0" y2="54.0"/><line class="grid" x1="50.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="50.0" y1="190.0" x2="400.0" y2="190.0"/><line class="line" x1="68.8" y1="190.0" x2="68.8" y2="20.0"/><text class="dim" x="68.8" y="203.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="100.0" y="203.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="131.2" y="203.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="162.5" y="203.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="193.8" y="203.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="225.0" y="203.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="256.2" y="203.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="287.5" y="203.0" font-size="9" text-anchor="middle">7</text><text class="dim" x="318.8" y="203.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="350.0" y="203.0" font-size="9" text-anchor="middle">9</text><text class="dim" x="381.2" y="203.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="63.8" y="125.0" font-size="9" text-anchor="end">0.1</text><text class="dim" x="63.8" y="57.0" font-size="9" text-anchor="end">0.2</text><rect class="dot2" opacity="0.6" x="57.8" y="156.1" width="21.9" height="33.9"/><rect class="dot2" opacity="0.6" x="89.1" y="88.4" width="21.8" height="101.6"/><rect class="dot2" opacity="0.6" x="120.3" y="37.7" width="21.9" height="152.3"/><rect class="dot2" opacity="0.6" x="151.6" y="37.7" width="21.8" height="152.3"/><rect class="dot2" opacity="0.6" x="182.8" y="75.7" width="21.9" height="114.3"/><rect class="dot2" opacity="0.6" x="214.1" y="121.4" width="21.8" height="68.6"/><rect class="dot2" opacity="0.6" x="245.3" y="155.7" width="21.9" height="34.3"/><rect class="dot2" opacity="0.6" x="276.6" y="175.3" width="21.8" height="14.7"/><rect class="dot2" opacity="0.6" x="307.8" y="184.5" width="21.9" height="5.5"/><rect class="dot2" opacity="0.6" x="339.1" y="188.2" width="21.8" height="1.8"/><rect class="dot2" opacity="0.6" x="370.3" y="189.4" width="21.9" height="0.6"/><text class="dim" x="400.0" y="218.0" font-size="10" text-anchor="end">number of events k</text><text class="ink" x="225" y="234" font-size="12" text-anchor="middle">Poisson(λ = 3): mean and variance 3</text></svg>
  <figcaption>An average of 3 orders an hour. 2 and 3 orders are the most likely (each ≈ 0.224); no order at all ≈ 0.05. There is a long tail to the right; 10 orders is not impossible but very rare.</figcaption>
</figure>

If an average of $3$ orders arrive per hour, the probability of none is
$e^{-3} \approx 0.050$, and of at least one $1 - 0.050 = 0.950$.

**From binomial to Poisson.** If the number of trials $n$ is very large, the
success probability $p$ very small and $np = \lambda$ fixed, the binomial
approaches the Poisson. That is why Poisson is the distribution for
counting rare events.

## The uniform and exponential distributions

**Uniform** on $[a, b]$: equal density $\frac{1}{b - a}$ everywhere;
$E[X] = \frac{a + b}{2}$, $\operatorname{Var}(X) = \frac{(b - a)^2}{12}$.

**The exponential distribution** describes the **waiting time** until the
next event. If events arrive at rate $\lambda$:

$$
f(x) = \lambda e^{-\lambda x} \quad (x \geq 0) \qquad P(X > t) = e^{-\lambda t} \qquad E[X] = \frac{1}{\lambda}
$$

<figure class="fig">
<svg viewBox="0 0 440 232" width="440"><line class="grid" x1="50.0" y1="200.0" x2="50.0" y2="20.0"/><line class="grid" x1="85.0" y1="200.0" x2="85.0" y2="20.0"/><line class="grid" x1="120.0" y1="200.0" x2="120.0" y2="20.0"/><line class="grid" x1="155.0" y1="200.0" x2="155.0" y2="20.0"/><line class="grid" x1="190.0" y1="200.0" x2="190.0" y2="20.0"/><line class="grid" x1="225.0" y1="200.0" x2="225.0" y2="20.0"/><line class="grid" x1="260.0" y1="200.0" x2="260.0" y2="20.0"/><line class="grid" x1="295.0" y1="200.0" x2="295.0" y2="20.0"/><line class="grid" x1="330.0" y1="200.0" x2="330.0" y2="20.0"/><line class="grid" x1="365.0" y1="200.0" x2="365.0" y2="20.0"/><line class="grid" x1="400.0" y1="200.0" x2="400.0" y2="20.0"/><line class="grid" x1="50.0" y1="200.0" x2="400.0" y2="200.0"/><line class="grid" x1="50.0" y1="167.3" x2="400.0" y2="167.3"/><line class="grid" x1="50.0" y1="134.5" x2="400.0" y2="134.5"/><line class="grid" x1="50.0" y1="101.8" x2="400.0" y2="101.8"/><line class="grid" x1="50.0" y1="69.1" x2="400.0" y2="69.1"/><line class="grid" x1="50.0" y1="36.4" x2="400.0" y2="36.4"/><line class="line" x1="50.0" y1="200.0" x2="400.0" y2="200.0"/><line class="line" x1="50.0" y1="200.0" x2="50.0" y2="20.0"/><text class="dim" x="120.0" y="213.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="190.0" y="213.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="260.0" y="213.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="330.0" y="213.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="45.0" y="121.2" font-size="9" text-anchor="end">0.25</text><text class="dim" x="45.0" y="39.4" font-size="9" text-anchor="end">0.5</text><polygon class="dot2" opacity="0.35" points="120.0,200.0 120.0,139.8 122.3,141.8 124.7,143.7 127.0,145.5 129.3,147.3 131.7,149.0 134.0,150.7 136.3,152.3 138.7,153.9 141.0,155.4 143.3,156.9 145.7,158.3 148.0,159.6 150.3,161.0 152.7,162.3 155.0,163.5 157.3,164.7 159.7,165.8 162.0,167.0 164.3,168.0 166.7,169.1 169.0,170.1 171.3,171.1 173.7,172.0 176.0,173.0 178.3,173.8 180.7,174.7 183.0,175.5 185.3,176.3 187.7,177.1 190.0,177.9 192.3,178.6 194.7,179.3 197.0,180.0 199.3,180.6 201.7,181.3 204.0,181.9 206.3,182.5 208.7,183.0 211.0,183.6 213.3,184.1 215.7,184.7 218.0,185.2 220.3,185.6 222.7,186.1 225.0,186.6 227.3,187.0 229.7,187.4 232.0,187.8 234.3,188.2 236.7,188.6 239.0,189.0 241.3,189.4 243.7,189.7 246.0,190.0 248.3,190.4 250.7,190.7 253.0,191.0 255.3,191.3 257.7,191.6 260.0,191.9 262.3,192.1 264.7,192.4 267.0,192.6 269.3,192.9 271.7,193.1 274.0,193.3 276.3,193.5 278.7,193.8 281.0,194.0 283.3,194.2 285.7,194.4 288.0,194.5 290.3,194.7 292.7,194.9 295.0,195.1 297.3,195.2 299.7,195.4 302.0,195.5 304.3,195.7 306.7,195.8 309.0,196.0 311.3,196.1 313.7,196.2 316.0,196.3 318.3,196.5 320.7,196.6 323.0,196.7 325.3,196.8 327.7,196.9 330.0,197.0 332.3,197.1 334.7,197.2 337.0,197.3 339.3,197.4 341.7,197.5 344.0,197.5 346.3,197.6 348.7,197.7 351.0,197.8 353.3,197.9 355.7,197.9 358.0,198.0 360.3,198.1 362.7,198.1 365.0,198.2 367.3,198.2 369.7,198.3 372.0,198.4 374.3,198.4 376.7,198.5 379.0,198.5 381.3,198.6 383.7,198.6 386.0,198.7 388.3,198.7 390.7,198.7 393.0,198.8 395.3,198.8 397.7,198.9 400.0,198.9 400.0,200.0"/><polyline class="curve" fill="none" points="50.0,36.4 51.5,39.7 52.9,43.0 54.4,46.3 55.8,49.4 57.3,52.6 58.8,55.6 60.2,58.6 61.7,61.5 63.1,64.3 64.6,67.1 66.0,69.9 67.5,72.6 69.0,75.2 70.4,77.8 71.9,80.3 73.3,82.7 74.8,85.2 76.2,87.5 77.7,89.9 79.2,92.1 80.6,94.3 82.1,96.5 83.5,98.7 85.0,100.7 86.5,102.8 87.9,104.8 89.4,106.8 90.8,108.7 92.3,110.6 93.8,112.4 95.2,114.2 96.7,116.0 98.1,117.7 99.6,119.4 101.0,121.1 102.5,122.7 104.0,124.3 105.4,125.9 106.9,127.4 108.3,128.9 109.8,130.4 111.2,131.8 112.7,133.2 114.2,134.6 115.6,135.9 117.1,137.2 118.5,138.5 120.0,139.8 121.5,141.0 122.9,142.3 124.4,143.4 125.8,144.6 127.3,145.8 128.8,146.9 130.2,148.0 131.7,149.0 133.1,150.1 134.6,151.1 136.0,152.1 137.5,153.1 139.0,154.1 140.4,155.0 141.9,156.0 143.3,156.9 144.8,157.8 146.2,158.6 147.7,159.5 149.2,160.3 150.6,161.1 152.1,161.9 153.5,162.7 155.0,163.5 156.5,164.2 157.9,165.0 159.4,165.7 160.8,166.4 162.3,167.1 163.8,167.8 165.2,168.4 166.7,169.1 168.1,169.7 169.6,170.4 171.0,171.0 172.5,171.6 174.0,172.2 175.4,172.7 176.9,173.3 178.3,173.8 179.8,174.4 181.2,174.9 182.7,175.4 184.2,175.9 185.6,176.4 187.1,176.9 188.5,177.4 190.0,177.9 191.5,178.3 192.9,178.8 194.4,179.2 195.8,179.6 197.3,180.0 198.8,180.5 200.2,180.9 201.7,181.3 203.1,181.6 204.6,182.0 206.0,182.4 207.5,182.8 209.0,183.1 210.4,183.5 211.9,183.8 213.3,184.1 214.8,184.5 216.2,184.8 217.7,185.1 219.2,185.4 220.6,185.7 222.1,186.0 223.5,186.3 225.0,186.6 226.5,186.8 227.9,187.1 229.4,187.4 230.8,187.6 232.3,187.9 233.8,188.1 235.2,188.4 236.7,188.6 238.1,188.9 239.6,189.1 241.0,189.3 242.5,189.5 244.0,189.8 245.4,190.0 246.9,190.2 248.3,190.4 249.8,190.6 251.2,190.8 252.7,191.0 254.2,191.1 255.6,191.3 257.1,191.5 258.5,191.7 260.0,191.9 261.5,192.0 262.9,192.2 264.4,192.3 265.8,192.5 267.3,192.7 268.8,192.8 270.2,193.0 271.7,193.1 273.1,193.2 274.6,193.4 276.0,193.5 277.5,193.7 279.0,193.8 280.4,193.9 281.9,194.0 283.3,194.2 284.8,194.3 286.2,194.4 287.7,194.5 289.2,194.6 290.6,194.7 292.1,194.8 293.5,195.0 295.0,195.1 296.5,195.2 297.9,195.3 299.4,195.4 300.8,195.5 302.3,195.5 303.8,195.6 305.2,195.7 306.7,195.8 308.1,195.9 309.6,196.0 311.0,196.1 312.5,196.2 314.0,196.2 315.4,196.3 316.9,196.4 318.3,196.5 319.8,196.5 321.2,196.6 322.7,196.7 324.2,196.7 325.6,196.8 327.1,196.9 328.5,196.9 330.0,197.0 331.5,197.1 332.9,197.1 334.4,197.2 335.8,197.2 337.3,197.3 338.8,197.4 340.2,197.4 341.7,197.5 343.1,197.5 344.6,197.6 346.0,197.6 347.5,197.7 349.0,197.7 350.4,197.8 351.9,197.8 353.3,197.9 354.8,197.9 356.2,197.9 357.7,198.0 359.2,198.0 360.6,198.1 362.1,198.1 363.5,198.1 365.0,198.2 366.5,198.2 367.9,198.3 369.4,198.3 370.8,198.3 372.3,198.4 373.8,198.4 375.2,198.4 376.7,198.5 378.1,198.5 379.6,198.5 381.0,198.6 382.5,198.6 384.0,198.6 385.4,198.6 386.9,198.7 388.3,198.7 389.8,198.7 391.2,198.8 392.7,198.8 394.2,198.8 395.6,198.8 397.1,198.9 398.5,198.9 400.0,198.9"/><text class="ink" x="92.0" y="62.5" font-size="11" text-anchor="start">f(x) = 0.5 e^(−0.5x)</text><text class="ink" x="242.5" y="160.7" font-size="11" text-anchor="middle">P(X > 2) = e⁻¹ ≈ 0.37</text><text class="dim" x="400.0" y="228.0" font-size="10" text-anchor="end">waiting time x</text></svg>
  <figcaption>An average of 0.5 customers per minute: the mean wait is 2 minutes. The probability of waiting more than 2 minutes, the shaded area, is e⁻¹ ≈ 0.37.</figcaption>
</figure>

**Memorylessness.** For the exponential distribution, "we have already
waited $5$ minutes" does not change the remaining wait:
$P(X > 5 + t \mid X > 5) = P(X > t)$. That is why the waiting times of
Poisson events are exponential.

## The normal distribution

The most important distribution. The normal distribution with mean $\mu$
and standard deviation $\sigma$ is a bell curve symmetric about $\mu$:

$$
f(x) = \frac{1}{\sigma \sqrt{2\pi}} \, e^{-\frac{(x - \mu)^2}{2\sigma^2}}
$$

It is written $X \sim \mathcal{N}(\mu, \sigma^2)$ for short.

<figure class="fig">
<svg viewBox="0 0 440 254" width="440"><line class="grid" x1="61.7" y1="230.0" x2="61.7" y2="60.0"/><line class="grid" x1="114.4" y1="230.0" x2="114.4" y2="60.0"/><line class="grid" x1="167.2" y1="230.0" x2="167.2" y2="60.0"/><line class="grid" x1="220.0" y1="230.0" x2="220.0" y2="60.0"/><line class="grid" x1="272.8" y1="230.0" x2="272.8" y2="60.0"/><line class="grid" x1="325.6" y1="230.0" x2="325.6" y2="60.0"/><line class="grid" x1="378.3" y1="230.0" x2="378.3" y2="60.0"/><line class="grid" x1="30.0" y1="230.0" x2="410.0" y2="230.0"/><line class="line" x1="30.0" y1="230.0" x2="410.0" y2="230.0"/><polygon class="dot" opacity="0.12" points="61.7,230.0 61.7,228.2 64.3,227.9 66.9,227.6 69.6,227.2 72.2,226.8 74.9,226.3 77.5,225.8 80.1,225.2 82.8,224.5 85.4,223.7 88.1,222.9 90.7,222.0 93.3,220.9 96.0,219.8 98.6,218.5 101.2,217.2 103.9,215.6 106.5,214.0 109.2,212.2 111.8,210.3 114.4,208.1 117.1,205.9 119.7,203.4 122.4,200.8 125.0,198.0 127.6,195.1 130.3,191.9 132.9,188.6 135.6,185.1 138.2,181.4 140.8,177.6 143.5,173.6 146.1,169.4 148.8,165.1 151.4,160.6 154.0,156.1 156.7,151.4 159.3,146.6 161.9,141.8 164.6,137.0 167.2,132.1 169.9,127.2 172.5,122.3 175.1,117.5 177.8,112.7 180.4,108.1 183.1,103.6 185.7,99.3 188.3,95.1 191.0,91.2 193.6,87.5 196.2,84.1 198.9,80.9 201.5,78.1 204.2,75.6 206.8,73.5 209.4,71.7 212.1,70.3 214.7,69.3 217.4,68.7 220.0,68.5 222.6,68.7 225.3,69.3 227.9,70.3 230.6,71.7 233.2,73.5 235.8,75.6 238.5,78.1 241.1,80.9 243.8,84.1 246.4,87.5 249.0,91.2 251.7,95.1 254.3,99.3 256.9,103.6 259.6,108.1 262.2,112.7 264.9,117.5 267.5,122.3 270.1,127.2 272.8,132.1 275.4,137.0 278.1,141.8 280.7,146.6 283.3,151.4 286.0,156.1 288.6,160.6 291.2,165.1 293.9,169.4 296.5,173.6 299.2,177.6 301.8,181.4 304.4,185.1 307.1,188.6 309.7,191.9 312.4,195.1 315.0,198.0 317.6,200.8 320.3,203.4 322.9,205.9 325.6,208.1 328.2,210.3 330.8,212.2 333.5,214.0 336.1,215.6 338.7,217.2 341.4,218.5 344.0,219.8 346.7,220.9 349.3,222.0 351.9,222.9 354.6,223.7 357.2,224.5 359.9,225.2 362.5,225.8 365.1,226.3 367.8,226.8 370.4,227.2 373.1,227.6 375.7,227.9 378.3,228.2 378.3,230.0"/><polygon class="dot" opacity="0.18" points="114.4,230.0 114.4,208.1 116.2,206.7 118.0,205.1 119.7,203.4 121.5,201.7 123.2,199.9 125.0,198.0 126.8,196.1 128.5,194.0 130.3,191.9 132.0,189.7 133.8,187.5 135.6,185.1 137.3,182.7 139.1,180.2 140.8,177.6 142.6,174.9 144.4,172.2 146.1,169.4 147.9,166.5 149.6,163.6 151.4,160.6 153.1,157.6 154.9,154.5 156.7,151.4 158.4,148.2 160.2,145.0 161.9,141.8 163.7,138.6 165.5,135.3 167.2,132.1 169.0,128.8 170.7,125.5 172.5,122.3 174.3,119.1 176.0,115.9 177.8,112.7 179.5,109.6 181.3,106.6 183.1,103.6 184.8,100.7 186.6,97.9 188.3,95.1 190.1,92.5 191.9,89.9 193.6,87.5 195.4,85.2 197.1,83.0 198.9,80.9 200.6,79.0 202.4,77.2 204.2,75.6 205.9,74.2 207.7,72.9 209.4,71.7 211.2,70.8 213.0,70.0 214.7,69.3 216.5,68.9 218.2,68.6 220.0,68.5 221.8,68.6 223.5,68.9 225.3,69.3 227.0,70.0 228.8,70.8 230.6,71.7 232.3,72.9 234.1,74.2 235.8,75.6 237.6,77.2 239.4,79.0 241.1,80.9 242.9,83.0 244.6,85.2 246.4,87.5 248.1,89.9 249.9,92.5 251.7,95.1 253.4,97.9 255.2,100.7 256.9,103.6 258.7,106.6 260.5,109.6 262.2,112.7 264.0,115.9 265.7,119.1 267.5,122.3 269.3,125.5 271.0,128.8 272.8,132.1 274.5,135.3 276.3,138.6 278.1,141.8 279.8,145.0 281.6,148.2 283.3,151.4 285.1,154.5 286.9,157.6 288.6,160.6 290.4,163.6 292.1,166.5 293.9,169.4 295.6,172.2 297.4,174.9 299.2,177.6 300.9,180.2 302.7,182.7 304.4,185.1 306.2,187.5 308.0,189.7 309.7,191.9 311.5,194.0 313.2,196.1 315.0,198.0 316.8,199.9 318.5,201.7 320.3,203.4 322.0,205.1 323.8,206.7 325.6,208.1 325.6,230.0"/><polygon class="dot" opacity="0.3" points="167.2,230.0 167.2,132.1 168.1,130.4 169.0,128.8 169.9,127.2 170.7,125.5 171.6,123.9 172.5,122.3 173.4,120.7 174.3,119.1 175.1,117.5 176.0,115.9 176.9,114.3 177.8,112.7 178.7,111.2 179.5,109.6 180.4,108.1 181.3,106.6 182.2,105.1 183.1,103.6 183.9,102.1 184.8,100.7 185.7,99.3 186.6,97.9 187.5,96.5 188.3,95.1 189.2,93.8 190.1,92.5 191.0,91.2 191.9,89.9 192.7,88.7 193.6,87.5 194.5,86.3 195.4,85.2 196.3,84.1 197.1,83.0 198.0,81.9 198.9,80.9 199.8,80.0 200.6,79.0 201.5,78.1 202.4,77.2 203.3,76.4 204.2,75.6 205.0,74.9 205.9,74.2 206.8,73.5 207.7,72.9 208.6,72.3 209.4,71.7 210.3,71.2 211.2,70.8 212.1,70.3 213.0,70.0 213.8,69.6 214.7,69.3 215.6,69.1 216.5,68.9 217.4,68.7 218.2,68.6 219.1,68.5 220.0,68.5 220.9,68.5 221.8,68.6 222.6,68.7 223.5,68.9 224.4,69.1 225.3,69.3 226.2,69.6 227.0,70.0 227.9,70.3 228.8,70.8 229.7,71.2 230.6,71.7 231.4,72.3 232.3,72.9 233.2,73.5 234.1,74.2 235.0,74.9 235.8,75.6 236.7,76.4 237.6,77.2 238.5,78.1 239.4,79.0 240.2,80.0 241.1,80.9 242.0,81.9 242.9,83.0 243.8,84.1 244.6,85.2 245.5,86.3 246.4,87.5 247.3,88.7 248.1,89.9 249.0,91.2 249.9,92.5 250.8,93.8 251.7,95.1 252.5,96.5 253.4,97.9 254.3,99.3 255.2,100.7 256.1,102.1 256.9,103.6 257.8,105.1 258.7,106.6 259.6,108.1 260.5,109.6 261.3,111.2 262.2,112.7 263.1,114.3 264.0,115.9 264.9,117.5 265.7,119.1 266.6,120.7 267.5,122.3 268.4,123.9 269.3,125.5 270.1,127.2 271.0,128.8 271.9,130.4 272.8,132.1 272.8,230.0"/><polyline class="curve" fill="none" points="30.0,229.8 31.6,229.7 33.2,229.7 34.7,229.7 36.3,229.6 37.9,229.6 39.5,229.5 41.1,229.5 42.7,229.4 44.2,229.4 45.8,229.3 47.4,229.2 49.0,229.2 50.6,229.1 52.2,229.0 53.8,228.9 55.3,228.8 56.9,228.6 58.5,228.5 60.1,228.4 61.7,228.2 63.3,228.0 64.8,227.9 66.4,227.7 68.0,227.4 69.6,227.2 71.2,227.0 72.8,226.7 74.3,226.4 75.9,226.1 77.5,225.8 79.1,225.4 80.7,225.0 82.2,224.6 83.8,224.2 85.4,223.7 87.0,223.3 88.6,222.7 90.2,222.2 91.8,221.6 93.3,220.9 94.9,220.3 96.5,219.6 98.1,218.8 99.7,218.0 101.2,217.2 102.8,216.3 104.4,215.3 106.0,214.3 107.6,213.3 109.2,212.2 110.7,211.0 112.3,209.8 113.9,208.6 115.5,207.3 117.1,205.9 118.7,204.4 120.2,202.9 121.8,201.4 123.4,199.7 125.0,198.0 126.6,196.3 128.2,194.5 129.8,192.6 131.3,190.6 132.9,188.6 134.5,186.5 136.1,184.4 137.7,182.2 139.2,179.9 140.8,177.6 142.4,175.2 144.0,172.7 145.6,170.2 147.2,167.7 148.8,165.1 150.3,162.4 151.9,159.7 153.5,157.0 155.1,154.2 156.7,151.4 158.2,148.6 159.8,145.7 161.4,142.8 163.0,139.9 164.6,137.0 166.2,134.0 167.8,131.1 169.3,128.1 170.9,125.2 172.5,122.3 174.1,119.4 175.7,116.5 177.2,113.7 178.8,110.9 180.4,108.1 182.0,105.4 183.6,102.7 185.2,100.1 186.8,97.6 188.3,95.1 189.9,92.7 191.5,90.4 193.1,88.2 194.7,86.1 196.2,84.1 197.8,82.2 199.4,80.3 201.0,78.7 202.6,77.1 204.2,75.6 205.8,74.3 207.3,73.1 208.9,72.0 210.5,71.1 212.1,70.3 213.7,69.7 215.2,69.2 216.8,68.8 218.4,68.6 220.0,68.5 221.6,68.6 223.2,68.8 224.7,69.2 226.3,69.7 227.9,70.3 229.5,71.1 231.1,72.0 232.7,73.1 234.2,74.3 235.8,75.6 237.4,77.1 239.0,78.7 240.6,80.3 242.2,82.2 243.8,84.1 245.3,86.1 246.9,88.2 248.5,90.4 250.1,92.7 251.7,95.1 253.2,97.6 254.8,100.1 256.4,102.7 258.0,105.4 259.6,108.1 261.2,110.9 262.8,113.7 264.3,116.5 265.9,119.4 267.5,122.3 269.1,125.2 270.7,128.1 272.2,131.1 273.8,134.0 275.4,137.0 277.0,139.9 278.6,142.8 280.2,145.7 281.8,148.6 283.3,151.4 284.9,154.2 286.5,157.0 288.1,159.7 289.7,162.4 291.2,165.1 292.8,167.7 294.4,170.2 296.0,172.7 297.6,175.2 299.2,177.6 300.8,179.9 302.3,182.2 303.9,184.4 305.5,186.5 307.1,188.6 308.7,190.6 310.2,192.6 311.8,194.5 313.4,196.3 315.0,198.0 316.6,199.7 318.2,201.4 319.8,202.9 321.3,204.4 322.9,205.9 324.5,207.3 326.1,208.6 327.7,209.8 329.2,211.0 330.8,212.2 332.4,213.3 334.0,214.3 335.6,215.3 337.2,216.3 338.7,217.2 340.3,218.0 341.9,218.8 343.5,219.6 345.1,220.3 346.7,220.9 348.2,221.6 349.8,222.2 351.4,222.7 353.0,223.3 354.6,223.7 356.2,224.2 357.8,224.6 359.3,225.0 360.9,225.4 362.5,225.8 364.1,226.1 365.7,226.4 367.2,226.7 368.8,227.0 370.4,227.2 372.0,227.4 373.6,227.7 375.2,227.9 376.7,228.0 378.3,228.2 379.9,228.4 381.5,228.5 383.1,228.6 384.7,228.8 386.2,228.9 387.8,229.0 389.4,229.1 391.0,229.2 392.6,229.2 394.2,229.3 395.8,229.4 397.3,229.4 398.9,229.5 400.5,229.5 402.1,229.6 403.7,229.6 405.2,229.7 406.8,229.7 408.4,229.7 410.0,229.8"/><text class="dim" x="61.7" y="245.0" font-size="10" text-anchor="middle">μ − 3σ</text><text class="dim" x="114.4" y="245.0" font-size="10" text-anchor="middle">μ − 2σ</text><text class="dim" x="167.2" y="245.0" font-size="10" text-anchor="middle">μ − σ</text><text class="dim" x="220.0" y="245.0" font-size="10" text-anchor="middle">μ</text><text class="dim" x="272.8" y="245.0" font-size="10" text-anchor="middle">μ + σ</text><text class="dim" x="325.6" y="245.0" font-size="10" text-anchor="middle">μ + 2σ</text><text class="dim" x="378.3" y="245.0" font-size="10" text-anchor="middle">μ + 3σ</text><text class="ink" x="220.0" y="169.3" font-size="11" text-anchor="middle">68 percent</text><line class="curve3" x1="114.4" y1="50.0" x2="325.6" y2="50.0"/><text class="ink" x="220.0" y="46.0" font-size="11" text-anchor="middle">95 percent</text><line class="curve3" x1="61.7" y1="30.0" x2="378.3" y2="30.0"/><text class="ink" x="220.0" y="26.0" font-size="11" text-anchor="middle">99.7 percent</text></svg>
  <figcaption>In a normal distribution 68 percent of the probability is within 1 standard deviation of the mean, 95 percent within 2 and 99.7 percent within 3. The curve dies away quickly on both sides.</figcaption>
</figure>

**The 68–95–99.7 rule.** If heights have mean $170$ cm and standard
deviation $10$ cm, about $68$ percent of people are between $160$ and
$180$, and $95$ percent between $150$ and $190$.

**The standard normal.** The transformation $Z = \frac{X - \mu}{\sigma}$
turns every normal distribution into $\mathcal{N}(0, 1)$; this is the
z-score of MATH 1. The cumulative probabilities of the standard normal are
ready in tables or software:

| $z$ | $0.5$ | $1$ | $1.5$ | $1.96$ | $2$ | $3$ |
|---|---|---|---|---|---|---|
| $P(Z \leq z)$ | $0.691$ | $0.841$ | $0.933$ | $0.975$ | $0.977$ | $0.999$ |

The probability of being taller than $190$ cm: $z = 2$, $1 - 0.977 =
0.023$.

**Why so common?** The sum of many small independent effects approaches a
normal distribution (the Central Limit Theorem, two sections ahead). That
is why height, measurement error and exam scores look like a bell curve.

## Summary table

| Distribution | Describes | $E[X]$ | $\operatorname{Var}(X)$ |
|---|---|---|---|
| Bernoulli($p$) | a single yes–no | $p$ | $p(1 - p)$ |
| Binomial($n, p$) | successes in $n$ trials | $np$ | $np(1 - p)$ |
| Poisson($\lambda$) | event count at a constant rate | $\lambda$ | $\lambda$ |
| Uniform($a, b$) | equal probability on an interval | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ |
| Exponential($\lambda$) | waiting time | $\frac{1}{\lambda}$ | $\frac{1}{\lambda^2}$ |
| Normal($\mu, \sigma^2$) | a sum of many small effects | $\mu$ | $\sigma^2$ |

## Distributions in machine learning

**Binary classification is Bernoulli.** Logistic regression predicts a $p$
for each example and treats the label as Bernoulli($p$). Log loss (binary
cross-entropy) comes from the likelihood of this Bernoulli model (the
Maximum Likelihood section).

**Multi-class classification is categorical.** Softmax gives a categorical
distribution over $k$ classes: the multi-class form of Bernoulli.

**Mean squared error is normal.** In linear regression, if the error is
assumed to be normally distributed, the best weights are exactly those
that minimise MSE.

**Count data is Poisson.** For targets such as numbers of clicks or visits,
Poisson regression is used.

**Initialisation and noise.** Neural network weights are usually
initialised at random from a normal or uniform distribution with small
variance; noise added in data augmentation is normal too.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>forgetting $\binom{n}{k}$ in the binomial</p>
      <p>Poisson variance $\sqrt{\lambda}$</p>
      <p>$P(X = 170)$ in a normal is $f(170)$</p>
      <p>all data is normal</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>which trials succeed must be chosen</p>
      <p>variance $\lambda$, standard deviation $\sqrt{\lambda}$</p>
      <p>a single point has probability $0$ in a continuous distribution</p>
      <p>income and waiting times are skewed</p>
    </div>
  </div>
  <figcaption>Before choosing a distribution, think about the process that makes the data: a count, a wait, or a sum of many small effects?</figcaption>
</figure>

- **Not checking the independence assumption.** Binomial and Poisson need
  independent trials; if one customer's purchase affects a friend's, the
  models go wrong.

## Summary

- Bernoulli: a single trial, $E = p$, $\operatorname{Var} = p(1 - p)$.
- Binomial: $\binom{n}{k} p^k (1 - p)^{n - k}$, $E = np$,
  $\operatorname{Var} = np(1 - p)$.
- Poisson: $\frac{e^{-\lambda}\lambda^k}{k!}$, mean and variance $\lambda$;
  counts of rare events.
- Exponential: waiting time, $P(X > t) = e^{-\lambda t}$, memoryless.
- Normal: the bell curve; 68–95–99.7; standardised with
  $Z = \frac{X - \mu}{\sigma}$.
- Classification is Bernoulli and categorical, MSE is normal, counts are
  Poisson.
