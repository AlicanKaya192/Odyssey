You can skip the division and take the logarithm of both sides straight away. The **product rule** splits the product on the left:

$$
\begin{aligned}
\ln (1000 \cdot 1.08^t) &= \ln 2500 \\
\ln 1000 + t \ln 1.08 &= \ln 2500
\end{aligned}
$$

$$
t = \frac{\ln 2500 - \ln 1000}{\ln 1.08}
$$

The numerator has the **quotient rule** hiding in it: $\ln 2500 - \ln 1000 = \ln \frac{2500}{1000} = \ln 2.5$. So you reach exactly the same formula as in the first path:

$$
t = \frac{\ln 2.5}{\ln 1.08} \approx 11.91
$$

The lesson of this path: dividing first is a shortcut; applied correctly, the rules give the same result without it.

**Careful:** expanding $\ln (1000 \cdot 1.08^t)$ as $t \cdot \ln (1000 \cdot 1.08)$ is **wrong**. The exponent sits only on $1.08$.

**Answer: about 11.91 years**
