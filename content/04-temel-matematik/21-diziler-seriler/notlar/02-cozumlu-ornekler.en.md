A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. The general term

**Question:** What is the fifth term of the sequence $a_n = n^2 - 1$?

$a_5 = 25 - 1 = 24$. With a general term you do not need the earlier terms.

## 2. A recursive sequence

**Question:** $a_1 = 2$ and $a_{n+1} = 3a_n - 1$. What are the first four
terms?

$a_2 = 3 \cdot 2 - 1 = 5$, $a_3 = 3 \cdot 5 - 1 = 14$, $a_4 = 3 \cdot 14 - 1 =
41$. The terms are $2, 5, 14, 41$.

## 3. An arithmetic sequence from two terms

**Question:** In an arithmetic sequence $a_3 = 11$ and $a_8 = 26$. What is
$a_{15}$?

$5$ steps between them, an increase of $15$: $d = 3$.
$a_1 = 11 - 2 \cdot 3 = 5$. $a_{15} = 5 + 14 \cdot 3 = 47$.

## 4. A geometric sequence from two terms

**Question:** In a geometric sequence $a_2 = 6$ and $a_5 = 162$. What are
$a_1$ and $r$?

$3$ steps between them: $r^3 = \frac{162}{6} = 27$, so $r = 3$.
$a_1 = \frac{6}{3} = 2$.

## 5. Expanding a Σ

**Question:** What is $\displaystyle \sum_{i=2}^{5} (2i - 1)$?

The counter takes $2, 3, 4, 5$: the terms are $3, 5, 7, 9$. The sum is
$24$. There are four terms: $5 - 2 + 1 = 4$.

## 6. With the Σ rules

**Question:** What is $\displaystyle \sum_{i=1}^{10} (3i + 2)$?

Split the sum and take the constant out:
$3 \sum_{i=1}^{10} i + \sum_{i=1}^{10} 2 = 3 \cdot 55 + 20 = 185$.

## 7. The sum of an arithmetic series

**Question:** What is $2 + 5 + 8 + \dots + 59$?

The number of terms is $\frac{59 - 2}{3} + 1 = 20$. The sum is
$\frac{20 \cdot (2 + 59)}{2} = 610$.

## 8. The sum of a geometric series

**Question:** What is $5 + 10 + 20 + \dots + 160$?

$r = 2$ and $160 = 5 \cdot 2^5$, so there are $6$ terms. The sum is
$5 \cdot \frac{1 - 2^6}{1 - 2} = 5 \cdot 63 = 315$.

## 9. Infinite geometric series

**Question:** What are $12 + 6 + 3 + \dots$ and $0.777\dots$?

In the first, $r = \frac{1}{2}$: $\frac{12}{1 - 1/2} = 24$. The second is
$\frac{7}{10} + \frac{7}{100} + \dots$ with $r = \frac{1}{10}$:
$\frac{7/10}{9/10} = \frac{7}{9}$.

## 10. Mean squared error

**Question:** The true values are $(4, 6, 10, 12)$ and the predictions
$(5, 6, 8, 12)$. What is the MSE?

The differences are $-1, 0, 2, 0$; their squares $1, 0, 4, 0$; the total is
$5$. $\text{MSE} = \frac{5}{4} = 1.25$.
