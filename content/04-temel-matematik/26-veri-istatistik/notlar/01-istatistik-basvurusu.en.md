A short version of everything in the lesson. Come back here when you get stuck on a question.

## Types of data

| Type | Example | Meaningful summary |
|---|---|---|
| continuous | height, price | mean, median, standard deviation |
| discrete | number of children | mean, median, mode |
| unordered categorical | city | mode, frequency table |
| ordered categorical | size | median, mode |

## Centre

| Measure | How | Sensitive to outliers? |
|---|---|---|
| mean | $\bar{x} = \frac{1}{n} \sum x_i$ | yes |
| median | sort, take the middle (mean of the two middle values if even) | no |
| mode | the most frequent value | no |

## Spread

| Measure | Formula |
|---|---|
| range | largest $-$ smallest |
| variance (population) | $\sigma^2 = \frac{1}{n} \sum (x_i - \bar{x})^2$ |
| variance (sample) | $s^2 = \frac{1}{n - 1} \sum (x_i - \bar{x})^2$ |
| standard deviation | the square root of the variance |
| IQR | Q3 $-$ Q1 |

Quartiles (the method in this section): the median splits the data in
two; Q1 is the median of the lower half, Q3 of the upper half.

## Outliers

Values below Q1 $- 1.5 \cdot$ IQR or above Q3 $+ 1.5 \cdot$ IQR are
outliers.

## Scaling

| Method | Formula | Result |
|---|---|---|
| z-score | $z = \dfrac{x - \bar{x}}{\sigma}$ | mean $0$, standard deviation $1$ |
| min–max | $x' = \dfrac{x - \min}{\max - \min}$ | between $0$ and $1$ |

The scaling values are computed from the training data only.

## Practical tips

- Always sort before taking the median.
- The deviations always add up to $0$: use this to check your work.
- For skewed data (salaries, prices) look at the median for a typical
  value.
- The standard deviation is in the data's unit; the variance in the unit
  squared.
