# Data and Basic Statistics

Statistics is the way to reduce a pile of numbers to a few meaningful
ones. Instead of reading a thousand students' marks one by one, saying "the
mean is $68$, most are between $55$ and $80$, and there are a few very low
marks" tells you what the data looks like. Every machine learning project
starts here: no model is built without looking at a column's mean, spread
and outliers, and the mean and standard deviation are used to bring features
to the same scale. In this section we will see types of data, summarising
with tables and graphs, measures of centre (mean, median, mode), measures of
spread (range, quartiles, variance, standard deviation), outliers and
standardisation.

Prerequisites: Decimals and Rounding, Roots, Sequences, Series and Sigma
Notation.

## Types of data

| Type | Meaning | Example |
|---|---|---|
| numerical, continuous | measured, can take any value | height, temperature, price |
| numerical, discrete | counted, whole numbers | number of children, clicks |
| categorical, unordered | a label with no order | colour, city |
| categorical, ordered | a label with an order | education level, size (S, M, L) |

Knowing the type tells you which summary makes sense: you do not take the
mean of cities, but you can count the most common one. In machine learning,
categorical columns are turned into numbers before being given to a model
(the encoding steps you will see in the Data Science path).

## Tables and histograms

A **frequency table** shows how many times each value or each range
occurs. When numerical data is split into ranges and drawn with bars it
becomes a **histogram**.

<figure class="fig">
<svg viewBox="0 0 440 234" width="440"><line class="grid" x1="67.5" y1="220.0" x2="67.5" y2="20.0"/><line class="grid" x1="111.2" y1="220.0" x2="111.2" y2="20.0"/><line class="grid" x1="155.0" y1="220.0" x2="155.0" y2="20.0"/><line class="grid" x1="198.8" y1="220.0" x2="198.8" y2="20.0"/><line class="grid" x1="242.5" y1="220.0" x2="242.5" y2="20.0"/><line class="grid" x1="286.2" y1="220.0" x2="286.2" y2="20.0"/><line class="grid" x1="330.0" y1="220.0" x2="330.0" y2="20.0"/><line class="grid" x1="373.8" y1="220.0" x2="373.8" y2="20.0"/><line class="grid" x1="50.0" y1="220.0" x2="400.0" y2="220.0"/><line class="grid" x1="50.0" y1="191.4" x2="400.0" y2="191.4"/><line class="grid" x1="50.0" y1="162.9" x2="400.0" y2="162.9"/><line class="grid" x1="50.0" y1="134.3" x2="400.0" y2="134.3"/><line class="grid" x1="50.0" y1="105.7" x2="400.0" y2="105.7"/><line class="grid" x1="50.0" y1="77.1" x2="400.0" y2="77.1"/><line class="grid" x1="50.0" y1="48.6" x2="400.0" y2="48.6"/><line class="grid" x1="50.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="50.0" y1="220.0" x2="400.0" y2="220.0"/><line class="line" x1="50.0" y1="220.0" x2="50.0" y2="20.0"/><text class="dim" x="67.5" y="233.0" font-size="9" text-anchor="middle">150</text><text class="dim" x="111.2" y="233.0" font-size="9" text-anchor="middle">155</text><text class="dim" x="155.0" y="233.0" font-size="9" text-anchor="middle">160</text><text class="dim" x="198.8" y="233.0" font-size="9" text-anchor="middle">165</text><text class="dim" x="242.5" y="233.0" font-size="9" text-anchor="middle">170</text><text class="dim" x="286.2" y="233.0" font-size="9" text-anchor="middle">175</text><text class="dim" x="330.0" y="233.0" font-size="9" text-anchor="middle">180</text><text class="dim" x="373.8" y="233.0" font-size="9" text-anchor="middle">185</text><text class="dim" x="45.0" y="194.4" font-size="9" text-anchor="end">2</text><text class="dim" x="45.0" y="137.3" font-size="9" text-anchor="end">6</text><text class="dim" x="45.0" y="80.1" font-size="9" text-anchor="end">10</text><text class="dim" x="45.0" y="23.0" font-size="9" text-anchor="end">14</text><rect class="dot" opacity="0.6" x="70.1" y="191.4" width="38.5" height="28.6"/><text class="ink" x="89.4" y="187.4" font-size="10" text-anchor="middle">2</text><rect class="dot" opacity="0.6" x="113.9" y="148.6" width="38.5" height="71.4"/><text class="ink" x="133.1" y="144.6" font-size="10" text-anchor="middle">5</text><rect class="dot" opacity="0.6" x="157.6" y="91.4" width="38.5" height="128.6"/><text class="ink" x="176.9" y="87.4" font-size="10" text-anchor="middle">9</text><rect class="dot" opacity="0.6" x="201.4" y="48.6" width="38.5" height="171.4"/><text class="ink" x="220.6" y="44.6" font-size="10" text-anchor="middle">12</text><rect class="dot" opacity="0.6" x="245.1" y="77.1" width="38.5" height="142.9"/><text class="ink" x="264.4" y="73.1" font-size="10" text-anchor="middle">10</text><rect class="dot" opacity="0.6" x="288.9" y="134.3" width="38.5" height="85.7"/><text class="ink" x="308.1" y="130.3" font-size="10" text-anchor="middle">6</text><rect class="dot" opacity="0.6" x="332.6" y="177.1" width="38.5" height="42.9"/><text class="ink" x="351.9" y="173.1" font-size="10" text-anchor="middle">3</text><text class="dim" x="400.0" y="214.0" font-size="10" text-anchor="end">height (cm)</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">number of students</text></svg>
  <figcaption>The heights of 47 students in 5 cm ranges. The busiest range is 165–170 (12 students); the counts fall towards the ends and the shape is a roughly symmetric hill.</figcaption>
</figure>

A histogram shows three things: the **centre** (where the values gather),
the **spread** (how wide an area they cover) and the **shape** (symmetric,
skewed to one side, one peak or several).

## Measures of centre

The **mean** is the sum of all values over the number of values:

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

The **median** is the middle value once the values are sorted; with an even
count, the mean of the two middle values. The **mode** is the most frequent
value.

The monthly salaries (thousand) of $7$ employees in a company: $20, 22,
25, 25, 28, 30, 150$. The mean is $\frac{300}{7} \approx 42.9$; the median
$25$ (the fourth value); the mode $25$.

<figure class="fig">
<svg viewBox="0 0 440 172" width="440"><line class="grid" x1="30.0" y1="140.0" x2="30.0" y2="30.0"/><line class="grid" x1="77.5" y1="140.0" x2="77.5" y2="30.0"/><line class="grid" x1="125.0" y1="140.0" x2="125.0" y2="30.0"/><line class="grid" x1="172.5" y1="140.0" x2="172.5" y2="30.0"/><line class="grid" x1="220.0" y1="140.0" x2="220.0" y2="30.0"/><line class="grid" x1="267.5" y1="140.0" x2="267.5" y2="30.0"/><line class="grid" x1="315.0" y1="140.0" x2="315.0" y2="30.0"/><line class="grid" x1="362.5" y1="140.0" x2="362.5" y2="30.0"/><line class="grid" x1="410.0" y1="140.0" x2="410.0" y2="30.0"/><line class="grid" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="30.0" y2="30.0"/><text class="dim" x="77.5" y="153.0" font-size="9" text-anchor="middle">20</text><text class="dim" x="125.0" y="153.0" font-size="9" text-anchor="middle">40</text><text class="dim" x="172.5" y="153.0" font-size="9" text-anchor="middle">60</text><text class="dim" x="220.0" y="153.0" font-size="9" text-anchor="middle">80</text><text class="dim" x="267.5" y="153.0" font-size="9" text-anchor="middle">100</text><text class="dim" x="315.0" y="153.0" font-size="9" text-anchor="middle">120</text><text class="dim" x="362.5" y="153.0" font-size="9" text-anchor="middle">140</text><text class="dim" x="410.0" y="153.0" font-size="9" text-anchor="middle">160</text><circle class="dot" cx="77.5" cy="121.7" r="6"/><circle class="dot" cx="82.2" cy="121.7" r="6"/><circle class="dot" cx="89.4" cy="121.7" r="6"/><circle class="dot" cx="89.4" cy="101.5" r="6"/><circle class="dot" cx="96.5" cy="121.7" r="6"/><circle class="dot" cx="101.2" cy="121.7" r="6"/><circle class="dot" cx="386.2" cy="121.7" r="6"/><line class="curve4" stroke-dasharray="5 4" x1="89.4" y1="140.0" x2="89.4" y2="44.7"/><line class="curve2" stroke-dasharray="5 4" x1="131.8" y1="140.0" x2="131.8" y2="44.7"/><text class="ink" x="85.4" y="40.7" font-size="11" text-anchor="end">median 25</text><text class="ink" x="135.8" y="40.7" font-size="11" text-anchor="start">mean ≈ 42.9</text><text class="dim" x="410.0" y="168.0" font-size="10" text-anchor="end">salary (thousand)</text></svg>
  <figcaption>Six salaries lie between 20 and 30 and one is 150. The single outlier pulls the mean to 42.9; none of the employees earns that much. The median stays at 25.</figcaption>
</figure>

**Which one when?** The mean takes every value into account, so it is
sensitive to outliers. The median looks only at the order and is not
affected by an outlier. For skewed data such as salaries or house prices the
median is the more honest "typical value". The mode is the only measure of
centre for categorical data.

## Measures of spread

Two datasets with the same mean can be very different.

<figure class="fig">
<svg viewBox="0 0 440 182" width="440"><line class="grid" x1="30.0" y1="140.0" x2="30.0" y2="20.0"/><line class="grid" x1="68.0" y1="140.0" x2="68.0" y2="20.0"/><line class="grid" x1="106.0" y1="140.0" x2="106.0" y2="20.0"/><line class="grid" x1="144.0" y1="140.0" x2="144.0" y2="20.0"/><line class="grid" x1="182.0" y1="140.0" x2="182.0" y2="20.0"/><line class="grid" x1="220.0" y1="140.0" x2="220.0" y2="20.0"/><line class="grid" x1="258.0" y1="140.0" x2="258.0" y2="20.0"/><line class="grid" x1="296.0" y1="140.0" x2="296.0" y2="20.0"/><line class="grid" x1="334.0" y1="140.0" x2="334.0" y2="20.0"/><line class="grid" x1="372.0" y1="140.0" x2="372.0" y2="20.0"/><line class="grid" x1="410.0" y1="140.0" x2="410.0" y2="20.0"/><line class="grid" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="30.0" y2="20.0"/><text class="dim" x="68.0" y="153.0" font-size="9" text-anchor="middle">30</text><text class="dim" x="144.0" y="153.0" font-size="9" text-anchor="middle">40</text><text class="dim" x="220.0" y="153.0" font-size="9" text-anchor="middle">50</text><text class="dim" x="296.0" y="153.0" font-size="9" text-anchor="middle">60</text><text class="dim" x="372.0" y="153.0" font-size="9" text-anchor="middle">70</text><line class="curve3" stroke-dasharray="5 4" x1="220.0" y1="140.0" x2="220.0" y2="20.0"/><circle class="dot" cx="204.8" cy="56.0" r="6"/><circle class="dot" cx="212.4" cy="56.0" r="6"/><circle class="dot" cx="220.0" cy="56.0" r="6"/><circle class="dot" cx="227.6" cy="56.0" r="6"/><circle class="dot" cx="235.2" cy="56.0" r="6"/><circle class="dot2" cx="68.0" cy="104.0" r="6"/><circle class="dot2" cx="144.0" cy="104.0" r="6"/><circle class="dot2" cx="220.0" cy="104.0" r="6"/><circle class="dot2" cx="296.0" cy="104.0" r="6"/><circle class="dot2" cx="372.0" cy="104.0" r="6"/><text class="ink" x="34.0" y="44.0" font-size="11" text-anchor="start">A: standard deviation ≈ 1.4</text><text class="ink" x="34.0" y="92.0" font-size="11" text-anchor="start">B: standard deviation ≈ 14.1</text><text class="ink" x="220" y="170" font-size="12" text-anchor="middle">both have mean 50</text></svg>
  <figcaption>Set A is packed between 48 and 52, set B spread out between 30 and 70. Both have mean 50; only a measure of spread shows the difference.</figcaption>
</figure>

The **range** is the largest minus the smallest. It is simple but looks at
only the two extremes; a single outlier inflates it.

The **variance** is the mean of the squared deviations from the mean:

$$
\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2
$$

The **standard deviation** is the square root of the variance, $\sigma$; in
the data's own unit it answers "how far from the mean are the values
typically".

**Example.** $2, 4, 4, 4, 5, 5, 7, 9$: the mean is $\frac{40}{8} = 5$.

| $x_i$ | $2$ | $4$ | $4$ | $4$ | $5$ | $5$ | $7$ | $9$ |
|---|---|---|---|---|---|---|---|---|
| $x_i - \bar{x}$ | $-3$ | $-1$ | $-1$ | $-1$ | $0$ | $0$ | $2$ | $4$ |
| $(x_i - \bar{x})^2$ | $9$ | $1$ | $1$ | $1$ | $0$ | $0$ | $4$ | $16$ |

The squares add up to $32$; the variance is $\frac{32}{8} = 4$ and the
standard deviation $2$.

**Why squares?** Adding the deviations themselves always gives $0$: those
above the mean exactly cancel those below. Squaring removes the sign.
Because of the square the unit is squared too; the square root brings the
unit back.

**$n - 1$ for a sample.** If the data is a sample from a population rather
than the whole population, the variance is computed with
$\frac{1}{n - 1} \sum (x_i - \bar{x})^2$: $\frac{32}{7} \approx 4.57$.
The sample mean lies closer to the data than the population mean does, so
the divisor is made a little smaller to correct for it. As the data grows
the difference becomes negligible; the Sampling section of the Advanced Mathematics module explains
why.

## Quartiles and box plots

Three numbers split sorted data into four equal parts: the **first
quartile** Q1, the **median** and the **third quartile** Q3. In this section
we find the quartiles like this: the median splits the data into two
halves; Q1 is the median of the lower half and Q3 the median of the upper
half. (Software may use slightly different methods; the results come out
close.)

The **interquartile range** $\text{IQR} = \text{Q3} - \text{Q1}$ is the
width of the middle half of the data. Unlike the range it does not look at
the extremes, so it is not affected by an outlier.

**Example.** $3, 5, 7, 8, 9, 11, 13, 15, 20, 40$: the median is
$\frac{9 + 11}{2} = 10$; the lower half $3, 5, 7, 8, 9$ gives Q1 $= 7$; the
upper half $11, 13, 15, 20, 40$ gives Q3 $= 15$. $\text{IQR} = 8$.

**The outlier rule.** A value more than $1.5 \cdot \text{IQR}$ below Q1 or
above Q3 counts as an outlier. Here the upper fence is $15 + 12 = 27$ and
the lower fence $7 - 12 = -5$: $40$ is an outlier.

<figure class="fig">
<svg viewBox="0 0 440 146" width="440"><line class="grid" x1="30.0" y1="130.0" x2="30.0" y2="30.0"/><line class="grid" x1="73.2" y1="130.0" x2="73.2" y2="30.0"/><line class="grid" x1="116.4" y1="130.0" x2="116.4" y2="30.0"/><line class="grid" x1="159.5" y1="130.0" x2="159.5" y2="30.0"/><line class="grid" x1="202.7" y1="130.0" x2="202.7" y2="30.0"/><line class="grid" x1="245.9" y1="130.0" x2="245.9" y2="30.0"/><line class="grid" x1="289.1" y1="130.0" x2="289.1" y2="30.0"/><line class="grid" x1="332.3" y1="130.0" x2="332.3" y2="30.0"/><line class="grid" x1="375.5" y1="130.0" x2="375.5" y2="30.0"/><line class="grid" x1="30.0" y1="130.0" x2="410.0" y2="130.0"/><line class="line" x1="30.0" y1="130.0" x2="410.0" y2="130.0"/><line class="line" x1="30.0" y1="130.0" x2="30.0" y2="30.0"/><text class="dim" x="73.2" y="143.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="116.4" y="143.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="159.5" y="143.0" font-size="9" text-anchor="middle">15</text><text class="dim" x="202.7" y="143.0" font-size="9" text-anchor="middle">20</text><text class="dim" x="245.9" y="143.0" font-size="9" text-anchor="middle">25</text><text class="dim" x="289.1" y="143.0" font-size="9" text-anchor="middle">30</text><text class="dim" x="332.3" y="143.0" font-size="9" text-anchor="middle">35</text><text class="dim" x="375.5" y="143.0" font-size="9" text-anchor="middle">40</text><rect class="dot" opacity="0.35" x="90.5" y="62.5" width="69.0" height="35.0"/><rect class="curve" fill="none" x="90.5" y="62.5" width="69.0" height="35.0"/><line class="curve2" stroke-width="3" x1="116.4" y1="97.5" x2="116.4" y2="62.5"/><line class="curve" x1="55.9" y1="80.0" x2="90.5" y2="80.0"/><line class="curve" x1="159.5" y1="80.0" x2="202.7" y2="80.0"/><line class="curve" x1="55.9" y1="90.0" x2="55.9" y2="70.0"/><line class="curve" x1="202.7" y1="90.0" x2="202.7" y2="70.0"/><line class="curve3" stroke-dasharray="5 4" x1="263.2" y1="110.0" x2="263.2" y2="50.0"/><circle class="dot2" cx="375.5" cy="80.0" r="6"/><text class="dim" x="55.9" y="62.0" font-size="10" text-anchor="middle">minimum</text><text class="ink" x="90.5" y="113.5" font-size="10" text-anchor="middle">Q1 = 7</text><text class="ink" x="116.4" y="54.5" font-size="10" text-anchor="middle">median 10</text><text class="ink" x="159.5" y="113.5" font-size="10" text-anchor="middle">Q3 = 15</text><text class="dim" x="263.2" y="44.0" font-size="10" text-anchor="middle">fence 27</text><text class="ink" x="375.5" y="68.0" font-size="10" text-anchor="middle">outlier 40</text><text class="dim" x="125.0" y="37.5" font-size="10" text-anchor="middle">IQR = 8</text></svg>
  <figcaption>The box runs from Q1 to Q3 and the line inside is the median. The whiskers reach the most extreme values inside the fences (3 and 20). 40 lies beyond the fence at 27; it is drawn as a separate point.</figcaption>
</figure>

## Standardisation

To compare numbers on different scales, each value is written as how many
standard deviations it lies from the mean. This is the **z-score**:

$$
z = \frac{x - \bar{x}}{\sigma}
$$

In an exam with mean $70$ and standard deviation $10$, a score of $85$ has
z-score $1.5$. In another exam with mean $60$ and standard deviation $5$, a
score of $70$ has z-score $2$: better in the second exam, because it is
further above its own class.

A standardised column has mean $0$ and standard deviation $1$.

**Min–max scaling** squeezes the values between $0$ and $1$:
$x' = \frac{x - \min}{\max - \min}$.

## Statistics in machine learning

**Getting to know the data.** The `describe`-style summaries you will see
in the Data Science path give, for each column, the count, mean, standard
deviation, minimum, quartiles and maximum; every number in this section is
there.

**Scaling.** Two features, floor area measured in hundreds and number of
rooms in ones, behave unevenly in distance-based methods ($k$-nearest
neighbours, k-means) and in gradient descent. Standardising with z-scores
or min–max scaling fixes this. The mean and standard deviation are computed
**from the training data only** and applied unchanged to the test data;
otherwise information leaks from the test data.

**Outliers.** Mean squared error (MSE) squares the deviations and is very
sensitive to outliers; mean absolute error (MAE), which behaves like the
median, is less so. An outlier that is a measurement error is cleaned out;
a real one is a situation the model has to learn.

**Imbalanced classes.** In data where $98$ percent of examples are
"normal", a model that calls everything "normal" gets $98$ percent accuracy
but has learned nothing. Looking at the frequency table of the classes
shows this in advance.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>typical value in skewed data = mean</p>
      <p>taking the median without sorting</p>
      <p>$\sigma = \sum (x_i - \bar{x}) / n$</p>
      <p>computing the scaling on all the data</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>in skewed data the median is more representative</p>
      <p>sort first, then take the middle</p>
      <p>square the deviations, then take the root</p>
      <p>compute it from the training data only</p>
    </div>
  </div>
  <figcaption>An outlier pulls the mean and the standard deviation, not the median or the IQR.</figcaption>
</figure>

- **Taking the mean of categorical data.** The mean of city codes means
  nothing; use the mode or a frequency table.
- **Mixing up standard deviation and variance.** The variance is in squared
  units; the standard deviation is in the data's own unit.

## Summary

- Data is numerical (continuous, discrete) or categorical (unordered,
  ordered).
- A histogram shows centre, spread and shape.
- Mean $\bar{x} = \frac{1}{n} \sum x_i$; median the middle of the sorted
  data; mode the most frequent value. An outlier pulls the mean, not the
  median.
- Variance $\frac{1}{n} \sum (x_i - \bar{x})^2$, standard deviation its
  square root; $n - 1$ for a sample.
- Quartiles and IQR; the $1.5 \cdot \text{IQR}$ rule marks outliers; a box
  plot draws them.
- $z = \frac{x - \bar{x}}{\sigma}$ puts scales on an equal footing; scaling
  is computed from the training data.
