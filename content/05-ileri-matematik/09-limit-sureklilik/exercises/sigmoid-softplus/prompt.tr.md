Sinir ağlarında iki aktivasyon: sigmoid $\sigma(x) = \dfrac{1}{1 + e^{-x}}$ ve softplus $s(x) = \ln(1 + e^x)$ (ReLU'nun yumuşak hâli).

1. $\lim_{x \to \infty} \sigma(x)$ kaçtır?
2. $\lim_{x \to -\infty} \sigma(x)$ kaçtır?
3. $\lim_{x \to \infty} \big(s(x) - x\big)$ kaçtır? (Büyük girdilerde softplus'ın ReLU'ya ne kadar yaklaştığını ölçüyor.)
