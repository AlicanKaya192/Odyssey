# Support Vector Machines

Many lines separate two classes. A **support vector machine (SVM)** picks the
"safest" one: the line passing **farthest** from the nearest points of the two
classes. This distance is the **margin**, and the points closest to the line,
which define the boundary, are the **support vectors**. In this section we
write a linear SVM from scratch with the hinge loss and subgradient descent and
compare it with scikit-learn's `SVC`; then we look at the kernel idea.

## The hinge loss

Labels `y ∈ {−1, +1}`, score `f(x) = w·x + b`. The **hinge loss** is
`max(0, 1 − y f(x))`: a sample on the right side and at least 1 away from the
boundary gets no penalty; one inside the margin or on the wrong side does. The
SVM minimises `λ/2 ‖w‖² + mean hinge loss`: if `‖w‖` is small, the margin
(`2 / ‖w‖`) is large.

<figure class="fig">
<svg viewBox="0 0 540 320" width="540" xmlns="http://www.w3.org/2000/svg"><circle class="dot2" cx="221.5" cy="122.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="221.1" cy="248.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="188.9" cy="143.8" r="3" fill-opacity=".75"/><circle class="dot" cx="287.2" cy="226.4" r="3" fill-opacity=".75"/><circle class="dot" cx="236.7" cy="174.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="240.6" cy="198.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="175.2" cy="256.0" r="3" fill-opacity=".75"/><circle class="dot" cx="328.2" cy="124.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="183.3" cy="212.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="174.9" cy="126.3" r="3" fill-opacity=".75"/><circle class="dot" cx="233.6" cy="112.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="164.4" cy="172.3" r="3" fill-opacity=".75"/><circle class="dot" cx="323.1" cy="102.6" r="3" fill-opacity=".75"/><circle class="dot" cx="355.3" cy="109.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="248.6" cy="260.4" r="3" fill-opacity=".75"/><circle class="dot" cx="373.0" cy="127.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="223.0" cy="136.6" r="3" fill-opacity=".75"/><circle class="dot" cx="380.2" cy="34.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="112.5" cy="242.1" r="3" fill-opacity=".75"/><circle class="dot" cx="373.5" cy="165.5" r="3" fill-opacity=".75"/><circle class="dot" cx="325.3" cy="46.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="243.7" cy="242.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="226.1" cy="174.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="209.8" cy="206.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="212.9" cy="265.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="212.3" cy="242.6" r="3" fill-opacity=".75"/><circle class="dot" cx="349.5" cy="100.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="169.5" cy="176.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="221.9" cy="203.8" r="3" fill-opacity=".75"/><circle class="dot" cx="363.5" cy="131.1" r="3" fill-opacity=".75"/><circle class="dot" cx="321.1" cy="114.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="204.5" cy="154.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="107.3" cy="215.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="122.4" cy="224.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="216.8" cy="202.9" r="3" fill-opacity=".75"/><circle class="dot" cx="372.5" cy="106.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="90.4" cy="250.7" r="3" fill-opacity=".75"/><circle class="dot" cx="396.6" cy="54.3" r="3" fill-opacity=".75"/><circle class="dot" cx="335.2" cy="185.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="296.0" cy="292.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="217.5" cy="206.7" r="3" fill-opacity=".75"/><circle class="dot" cx="340.5" cy="170.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="187.2" cy="159.9" r="3" fill-opacity=".75"/><circle class="dot" cx="309.2" cy="179.4" r="3" fill-opacity=".75"/><circle class="dot" cx="328.9" cy="117.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="197.7" cy="238.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="226.1" cy="211.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="153.9" cy="196.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="202.1" cy="199.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="131.7" cy="238.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="222.7" cy="166.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="218.3" cy="198.4" r="3" fill-opacity=".75"/><circle class="dot" cx="360.6" cy="79.4" r="3" fill-opacity=".75"/><circle class="dot" cx="404.8" cy="100.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="181.0" cy="183.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="123.2" cy="201.2" r="3" fill-opacity=".75"/><circle class="dot" cx="313.0" cy="120.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="226.6" cy="200.8" r="3" fill-opacity=".75"/><circle class="dot" cx="271.2" cy="133.8" r="3" fill-opacity=".75"/><circle class="dot" cx="298.6" cy="119.5" r="3" fill-opacity=".75"/><circle class="dot" cx="347.6" cy="159.0" r="3" fill-opacity=".75"/><circle class="dot" cx="363.4" cy="63.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="195.3" cy="171.7" r="3" fill-opacity=".75"/><circle class="dot" cx="270.4" cy="141.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="247.2" cy="276.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="185.5" cy="239.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="255.0" cy="154.1" r="3" fill-opacity=".75"/><circle class="dot" cx="306.6" cy="113.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="97.0" cy="166.5" r="3" fill-opacity=".75"/><circle class="dot" cx="347.5" cy="62.5" r="3" fill-opacity=".75"/><circle class="dot" cx="232.5" cy="103.6" r="3" fill-opacity=".75"/><circle class="dot2" cx="191.9" cy="311.9" r="3" fill-opacity=".75"/><circle class="dot" cx="303.7" cy="121.6" r="3" fill-opacity=".75"/><circle class="dot" cx="366.5" cy="110.0" r="3" fill-opacity=".75"/><circle class="dot" cx="311.1" cy="99.6" r="3" fill-opacity=".75"/><circle class="dot" cx="328.2" cy="145.6" r="3" fill-opacity=".75"/><circle class="dot" cx="289.9" cy="112.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="213.3" cy="124.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="187.8" cy="134.8" r="3" fill-opacity=".75"/><circle class="dot" cx="347.5" cy="68.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="168.8" cy="238.9" r="3" fill-opacity=".75"/><circle class="dot" cx="319.9" cy="80.5" r="3" fill-opacity=".75"/><circle class="dot" cx="340.3" cy="86.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="220.3" cy="158.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="215.3" cy="224.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="228.6" cy="198.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="280.4" cy="208.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="211.6" cy="214.9" r="3" fill-opacity=".75"/><circle class="dot" cx="381.6" cy="81.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="234.3" cy="254.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="143.3" cy="190.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="237.3" cy="139.9" r="3" fill-opacity=".75"/><circle class="dot" cx="257.6" cy="125.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="136.0" cy="242.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="197.7" cy="161.6" r="3" fill-opacity=".75"/><circle class="dot" cx="310.9" cy="148.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="193.6" cy="149.2" r="3" fill-opacity=".75"/><circle class="dot" cx="434.5" cy="182.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="195.5" cy="220.1" r="3" fill-opacity=".75"/><circle class="dot" cx="382.1" cy="99.7" r="3" fill-opacity=".75"/><circle class="dot" cx="397.7" cy="160.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="207.6" cy="221.1" r="3" fill-opacity=".75"/><circle class="dot" cx="287.0" cy="124.6" r="3" fill-opacity=".75"/><circle class="dot" cx="283.3" cy="26.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="224.5" cy="244.7" r="3" fill-opacity=".75"/><circle class="dot" cx="307.5" cy="45.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="186.9" cy="172.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="231.5" cy="156.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="233.7" cy="210.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="182.2" cy="276.6" r="3" fill-opacity=".75"/><circle class="dot" cx="331.0" cy="112.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="191.9" cy="208.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="156.0" cy="110.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="186.0" cy="245.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="181.9" cy="209.1" r="3" fill-opacity=".75"/><circle class="dot" cx="364.2" cy="219.9" r="3" fill-opacity=".75"/><circle class="dot" cx="354.7" cy="143.9" r="3" fill-opacity=".75"/><circle class="dot" cx="325.5" cy="75.3" r="3" fill-opacity=".75"/><circle class="dot" cx="365.2" cy="146.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="203.1" cy="123.3" r="3" fill-opacity=".75"/><circle class="dot" cx="390.3" cy="81.4" r="3" fill-opacity=".75"/><circle class="dot" cx="333.5" cy="77.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="223.8" cy="224.9" r="3" fill-opacity=".75"/><circle class="dot" cx="291.1" cy="95.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="223.2" cy="151.1" r="3" fill-opacity=".75"/><circle class="dot" cx="312.9" cy="58.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="191.8" cy="149.1" r="3" fill-opacity=".75"/><circle class="dot" cx="356.1" cy="142.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="167.4" cy="206.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="196.1" cy="162.3" r="3" fill-opacity=".75"/><circle class="dot" cx="304.1" cy="179.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="206.4" cy="121.1" r="3" fill-opacity=".75"/><circle class="dot" cx="402.0" cy="144.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="195.6" cy="188.5" r="3" fill-opacity=".75"/><circle class="dot" cx="305.3" cy="128.1" r="3" fill-opacity=".75"/><circle class="dot" cx="321.6" cy="162.0" r="3" fill-opacity=".75"/><circle class="dot" cx="307.2" cy="138.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="217.0" cy="251.6" r="3" fill-opacity=".75"/><circle class="dot2" cx="211.6" cy="243.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="173.2" cy="249.1" r="3" fill-opacity=".75"/><circle class="dot" cx="501.6" cy="65.1" r="3" fill-opacity=".75"/><circle class="dot" cx="389.6" cy="83.7" r="3" fill-opacity=".75"/><circle class="dot" cx="323.2" cy="115.0" r="3" fill-opacity=".75"/><circle class="dot" cx="345.3" cy="99.1" r="3" fill-opacity=".75"/><circle class="dot" cx="358.1" cy="53.8" r="3" fill-opacity=".75"/><circle class="dot" cx="208.8" cy="141.2" r="3" fill-opacity=".75"/><circle class="dot" cx="361.6" cy="132.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="200.5" cy="139.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="215.2" cy="127.0" r="3" fill-opacity=".75"/><circle class="dot" cx="331.3" cy="107.9" r="3" fill-opacity=".75"/><circle class="dot" cx="288.3" cy="201.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="189.5" cy="199.3" r="3" fill-opacity=".75"/><circle class="dot" cx="318.6" cy="174.6" r="3" fill-opacity=".75"/><circle class="dot" cx="360.7" cy="114.9" r="3" fill-opacity=".75"/><circle class="dot" cx="333.5" cy="150.6" r="3" fill-opacity=".75"/><circle class="dot2" cx="276.3" cy="139.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="220.0" cy="206.8" r="3" fill-opacity=".75"/><circle class="dot" cx="343.7" cy="46.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="325.1" cy="201.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="189.1" cy="278.1" r="3" fill-opacity=".75"/><circle class="dot2" cx="324.6" cy="248.4" r="3" fill-opacity=".75"/><circle class="dot" cx="369.7" cy="96.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="263.1" cy="238.1" r="3" fill-opacity=".75"/><circle class="dot" cx="265.0" cy="111.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="224.3" cy="153.6" r="3" fill-opacity=".75"/><circle class="dot2" cx="136.2" cy="221.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="196.0" cy="258.8" r="3" fill-opacity=".75"/><circle class="dot" cx="326.2" cy="84.3" r="3" fill-opacity=".75"/><circle class="dot" cx="331.6" cy="178.4" r="3" fill-opacity=".75"/><circle class="dot2" cx="221.6" cy="165.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="229.6" cy="168.7" r="3" fill-opacity=".75"/><circle class="dot" cx="263.6" cy="98.5" r="3" fill-opacity=".75"/><circle class="dot" cx="358.3" cy="133.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="204.8" cy="234.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="259.0" cy="214.4" r="3" fill-opacity=".75"/><circle class="dot" cx="293.4" cy="110.0" r="3" fill-opacity=".75"/><circle class="dot2" cx="211.8" cy="173.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="172.0" cy="230.3" r="3" fill-opacity=".75"/><circle class="dot" cx="349.2" cy="23.9" r="3" fill-opacity=".75"/><circle class="dot" cx="352.8" cy="175.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="214.2" cy="234.6" r="3" fill-opacity=".75"/><circle class="dot2" cx="129.3" cy="230.7" r="3" fill-opacity=".75"/><circle class="dot" cx="308.9" cy="100.3" r="3" fill-opacity=".75"/><circle class="dot" cx="388.7" cy="70.0" r="3" fill-opacity=".75"/><circle class="dot" cx="367.2" cy="136.1" r="3" fill-opacity=".75"/><circle class="dot" cx="339.7" cy="119.5" r="3" fill-opacity=".75"/><circle class="dot" cx="392.4" cy="145.3" r="3" fill-opacity=".75"/><circle class="dot" cx="310.0" cy="54.9" r="3" fill-opacity=".75"/><circle class="dot2" cx="231.4" cy="220.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="214.1" cy="195.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="215.1" cy="168.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="222.6" cy="209.5" r="3" fill-opacity=".75"/><circle class="dot" cx="311.9" cy="190.5" r="3" fill-opacity=".75"/><circle class="dot2" cx="188.8" cy="153.7" r="3" fill-opacity=".75"/><circle class="dot2" cx="216.8" cy="229.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="197.0" cy="237.8" r="3" fill-opacity=".75"/><circle class="dot2" cx="219.4" cy="117.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="283.3" cy="151.3" r="3" fill-opacity=".75"/><circle class="dot2" cx="240.2" cy="211.2" r="3" fill-opacity=".75"/><circle class="dot2" cx="155.1" cy="201.2" r="3" fill-opacity=".75"/><line class="curve" x1="18.0" y1="-279.1" x2="522.0" y2="614.2"/><line class="curve3" x1="18.0" y1="-336.8" x2="522.0" y2="556.5"/><line class="curve3" x1="18.0" y1="-221.3" x2="522.0" y2="672.0"/><circle class="curve" cx="221.5" cy="122.9" r="6" fill="none"/><circle class="curve" cx="223.0" cy="136.6" r="6" fill="none"/><circle class="curve" cx="255.0" cy="154.1" r="6" fill="none"/><circle class="curve" cx="213.3" cy="124.9" r="6" fill="none"/><circle class="curve" cx="280.4" cy="208.7" r="6" fill="none"/><circle class="curve" cx="237.3" cy="139.9" r="6" fill="none"/><circle class="curve" cx="231.5" cy="156.1" r="6" fill="none"/><circle class="curve" cx="215.2" cy="127.0" r="6" fill="none"/><circle class="curve" cx="276.3" cy="139.9" r="6" fill="none"/><circle class="curve" cx="325.1" cy="201.4" r="6" fill="none"/><circle class="curve" cx="324.6" cy="248.4" r="6" fill="none"/><circle class="curve" cx="219.4" cy="117.3" r="6" fill="none"/><circle class="curve" cx="283.3" cy="151.3" r="6" fill="none"/><circle class="curve" cx="287.2" cy="226.4" r="6" fill="none"/><circle class="curve" cx="236.7" cy="174.2" r="6" fill="none"/><circle class="curve" cx="233.6" cy="112.9" r="6" fill="none"/><circle class="curve" cx="309.2" cy="179.4" r="6" fill="none"/><circle class="curve" cx="271.2" cy="133.8" r="6" fill="none"/><circle class="curve" cx="270.4" cy="141.0" r="6" fill="none"/><circle class="curve" cx="232.5" cy="103.6" r="6" fill="none"/><circle class="curve" cx="257.6" cy="125.2" r="6" fill="none"/><circle class="curve" cx="304.1" cy="179.9" r="6" fill="none"/><circle class="curve" cx="208.8" cy="141.2" r="6" fill="none"/><circle class="curve" cx="288.3" cy="201.4" r="6" fill="none"/><circle class="curve" cx="265.0" cy="111.7" r="6" fill="none"/><circle class="curve" cx="263.6" cy="98.5" r="6" fill="none"/><circle class="curve" cx="311.9" cy="190.5" r="6" fill="none"/></svg>
<figcaption>Two classes, purple and orange. The thick line is the SVM boundary, the dashed lines the edges of the margin (f(x) = ±1). The 27 ringed points are the support vectors: only they define the boundary.</figcaption>
</figure>

The loss is not differentiable everywhere; where the hinge bends, a
**subgradient** is used. This method, which walks the samples one by one and
shrinks the step size as `1 / (λ t)`, is a form of the Pegasos algorithm.

```python
import numpy as np

rng = np.random.default_rng(13)
n = 200
y = np.where(rng.random(n) < 0.5, 1, -1)
X = rng.normal(0, 1, (n, 2)) + np.outer(y, [1.5, 1.0])


def hinge_svm(X, y, lam, epochs, seed=0):
    order_rng = np.random.default_rng(seed)
    w, b = np.zeros(X.shape[1]), 0.0
    t = 0
    for _ in range(epochs):
        for i in order_rng.permutation(len(y)):
            t += 1
            lr = 1 / (lam * t)
            # inside the margin or wrong
            if y[i] * (X[i] @ w + b) < 1:
                w = (1 - lr * lam) * w + lr * y[i] * X[i]
                b += lr * y[i]
            else:                                       # only shrink
                w = (1 - lr * lam) * w
    return w, b


from sklearn.svm import SVC

lam = 0.01
w, b = hinge_svm(X, y, lam, 50)
C = 1 / (lam * n)                                       # scikit-learn's scale
ref = SVC(kernel="linear", C=C).fit(X, y)
wr, br = ref.coef_[0], ref.intercept_[0]
cos = w @ wr / np.linalg.norm(w) / np.linalg.norm(wr)
print(w.round(3), round(b, 3))
print(wr.round(3), round(br, 3), round(cos, 4))
pred = np.sign(X @ w + b)
print((pred == ref.predict(X)).mean(), round((pred == y).mean(), 3))
```

```text
[1.294 0.75 ] 0.178
[1.29  0.728] 0.131 0.9999
0.99 0.96
```

The link between scikit-learn's `C` and our `λ` is `C = 1 / (λ n)`. Our weights
(1.294, 0.75) and `SVC`'s (1.29, 0.728) are almost the same; the cosine between
their directions is 0.9999. The subgradient method gets near the bottom, not
exactly onto it; 99% of the predictions match.

## Margin and support vectors

```python
margin = y * (X @ wr + br)
print(round(2 / np.linalg.norm(wr), 3), int((margin <= 1 + 1e-6).sum()),
      int(ref.n_support_.sum()))
```

```text
1.351 25 27
```

The margin's width is 1.351. There are 25 samples with `y f(x) ≤ 1`, that is,
on the boundary or inside the margin; scikit-learn counts 27 support vectors
(those right on the edge with a small tolerance). The key point: the SVM's
decision depends only on these few samples; if we deleted the other 175, the
line would not change.

## C: between margin and error

```python
for c in (0.01, 1.0, 100.0):
    m = SVC(kernel="linear", C=c).fit(X, y)
    width = 2 / np.linalg.norm(m.coef_[0])
    print(c, round(width, 3), int(m.n_support_.sum()), round(m.score(X, y), 3))
```

```text
0.01 3.109 78 0.95
1.0 1.217 24 0.955
100.0 0.869 21 0.965
```

A small `C` (strong regularisation) accepts a wide margin (3.1) and 78 support
vectors: it tolerates many points entering the margin. A large `C` is strict
about errors: the margin narrows to 0.87. `C` is again chosen with
cross-validation.

## The kernel idea: a non-linear boundary

If the class is the inside of a circle, no line can separate it. But if we
widen the feature space (add `x₁²`, `x₂²`), the circle is separated by a
**plane** in the new space. A **kernel** SVM does this widening without doing
it explicitly, only by replacing the points' inner products with a function
(like RBF).

```python
Xc = rng.uniform(-3, 3, (300, 2))
yc = np.where(Xc[:, 0] ** 2 + Xc[:, 1] ** 2 < 4, 1, -1)
Xct = rng.uniform(-3, 3, (1000, 2))
yct = np.where(Xct[:, 0] ** 2 + Xct[:, 1] ** 2 < 4, 1, -1)
lin = SVC(kernel="linear", C=1.0).fit(Xc, yc)
rbf = SVC(kernel="rbf", C=1.0).fit(Xc, yc)
print(round(lin.score(Xct, yct), 3), round(rbf.score(Xct, yct), 3))
phi = lambda Z: np.column_stack([Z, Z ** 2])           # an explicit widening
w2, b2 = hinge_svm(phi(Xc), yc, 0.001, 50)
print(round((np.sign(phi(Xct) @ w2 + b2) == yct).mean(), 3))
```

```text
0.641 0.976
0.939
```

The linear SVM stays at 64.1%. The SVM with an RBF kernel gets 97.6%. Our
linear SVM gets 93.9% once the squared features are added: we did the kernel's
job by hand. A kernel makes even an infinite-dimensional widening (RBF)
computable.

## Summary

- An SVM looks for the boundary that maximises the margin between two classes.
- Loss: `λ/2 ‖w‖² + mean(max(0, 1 − y f(x)))`; solved with subgradient
  descent.
- The decision depends only on the support vectors.
- `C = 1/(λn)`: a small `C` gives a wide margin with many violations, a large
  `C` a narrow margin.
- A kernel widens the feature space through inner products; non-linear
  boundaries.
- Since it rests on distance, features are standardised.
