# Principal Component Analysis (PCA)

In data with many features, most features are related to each other: they
measure one thing twice, three times. **Principal component analysis** (PCA)
rotates the data onto new axes. The first axis is the direction in which the
data is **most spread out**, the second is the most spread-out direction
perpendicular to it, and so on. If most of the spread gathers in the first few
axes, we can drop the rest and **reduce the dimension** (dimensionality
reduction). In this section we write PCA from scratch with the eigenvectors of
the covariance matrix and compare it with scikit-learn's `PCA`.

## Covariance and eigenvectors

PCA is four steps:

1. Subtract each feature's mean (**centre** the data).
2. Compute the **covariance matrix**: how the features change together.
3. The **eigenvectors** of this matrix are the new axes, the **eigenvalues**
   the variance along each axis. Sort from large to small.
4. Project the data onto the new axes.

```python
import numpy as np
from sklearn.decomposition import PCA

rng = np.random.default_rng(17)
t = rng.normal(0, 1, 300)
X = np.column_stack([2 * t + rng.normal(0, 0.5, 300),
                     t + rng.normal(0, 0.8, 300)]) + [3, 1]

Xc = X - X.mean(axis=0)                      # 1) centre
C = Xc.T @ Xc / (len(X) - 1)                 # 2) the covariance matrix
vals, vecs = np.linalg.eigh(C)               # 3) eigenvalues, eigenvectors
order = np.argsort(vals)[::-1]               # from large to small
vals, vecs = vals[order], vecs[:, order]
print(C.round(3))
print(vals.round(3), (vals / vals.sum()).round(3))
print(vecs.T.round(3))
ref = PCA().fit(X)
print(ref.explained_variance_.round(3), ref.explained_variance_ratio_.round(3))
print(ref.components_.round(3))
Z = Xc @ vecs                                # 4) project onto the new axes
r = np.corrcoef(Z.T)[0, 1]
print(Z.var(axis=0, ddof=1).round(3), round(abs(float(r)), 6))
```

```text
[[4.079 1.91 ]
 [1.91  1.559]]
[5.107 0.531] [0.906 0.094]
[[-0.881 -0.474]
 [ 0.474 -0.881]]
[5.107 0.531] [0.906 0.094]
[[ 0.881  0.474]
 [-0.474  0.881]]
[5.107 0.531] 0.0
```

The two features are related (covariance 1.91). The first component's
variance is 5.107, the second's 0.531: **90.6%** of the total spread lies in a
single direction. That direction is (0.881, 0.474); since the data was
generated as `x ≈ 2t`, `y ≈ t`, it is close to the direction (2, 1).
scikit-learn found the same variances and the same explained ratios. The signs
of the axes are flipped: an eigenvector's direction is arbitrary, `v` and `−v`
define the same axis; scikit-learn picks the sign by its own rule. The
variances of the new coordinates (`Z`) equal the eigenvalues and their
correlation is 0: PCA turns related features into **uncorrelated** axes.

<figure class="fig">
<svg viewBox="0 0 480 300" width="480" xmlns="http://www.w3.org/2000/svg"><circle class="dot" cx="327.8" cy="146.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="272.6" cy="196.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="203.4" cy="196.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="166.7" cy="245.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="110.3" cy="233.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="255.6" cy="137.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="181.3" cy="177.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="173.6" cy="193.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="229.4" cy="146.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="217.5" cy="153.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="65.4" cy="269.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="304.5" cy="125.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="77.0" cy="225.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="324.1" cy="109.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="266.0" cy="131.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="186.4" cy="211.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="346.4" cy="110.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="201.0" cy="152.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="269.9" cy="139.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="270.4" cy="173.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="270.4" cy="122.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="305.6" cy="155.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="156.7" cy="218.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="158.6" cy="175.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="258.7" cy="128.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="202.6" cy="152.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="20.0" cy="253.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="369.1" cy="82.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="52.4" cy="265.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="103.0" cy="237.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="141.9" cy="232.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="254.5" cy="182.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="367.1" cy="94.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="251.2" cy="186.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="182.2" cy="188.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="228.1" cy="186.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="205.4" cy="138.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="240.5" cy="152.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="154.4" cy="232.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="238.1" cy="134.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="263.9" cy="153.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="36.6" cy="277.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="211.6" cy="194.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="261.8" cy="135.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="261.0" cy="157.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="185.5" cy="186.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="131.7" cy="234.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="167.8" cy="188.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="275.9" cy="135.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="183.6" cy="185.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="191.6" cy="184.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="302.8" cy="98.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="206.7" cy="174.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="179.6" cy="216.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="244.3" cy="123.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="266.0" cy="174.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="300.1" cy="147.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="169.2" cy="199.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="122.1" cy="200.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="230.1" cy="158.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="311.0" cy="175.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="160.4" cy="234.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="261.1" cy="158.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="289.2" cy="149.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="281.1" cy="152.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="238.8" cy="209.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="200.4" cy="176.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="176.7" cy="189.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="162.0" cy="231.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="299.4" cy="179.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="149.0" cy="202.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="330.5" cy="101.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="140.0" cy="253.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="460.0" cy="72.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="119.7" cy="192.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="357.8" cy="64.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="192.2" cy="197.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="223.9" cy="236.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="230.8" cy="165.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="213.5" cy="165.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="412.4" cy="15.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="213.9" cy="135.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="141.1" cy="193.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="308.8" cy="151.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="294.4" cy="183.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="173.6" cy="231.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="245.8" cy="173.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="247.4" cy="181.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="257.3" cy="116.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="298.7" cy="138.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="211.9" cy="225.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="230.6" cy="191.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="288.0" cy="100.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="259.4" cy="132.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="132.1" cy="178.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="195.0" cy="218.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="171.9" cy="174.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="228.8" cy="187.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="390.5" cy="116.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="251.6" cy="201.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="264.3" cy="201.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="358.1" cy="155.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="265.1" cy="145.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="297.0" cy="157.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="355.5" cy="134.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="260.0" cy="125.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="266.9" cy="171.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="268.5" cy="126.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="247.3" cy="184.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="208.9" cy="226.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="134.9" cy="223.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="220.9" cy="188.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="307.5" cy="126.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="211.2" cy="175.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="324.9" cy="78.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="262.9" cy="179.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="184.7" cy="215.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="58.7" cy="249.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="253.5" cy="124.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="168.3" cy="128.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="99.0" cy="256.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="265.1" cy="134.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="222.7" cy="220.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="264.2" cy="156.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="210.0" cy="220.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="247.3" cy="176.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="198.3" cy="227.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="335.5" cy="93.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="272.1" cy="136.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="127.2" cy="205.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="278.8" cy="187.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="207.3" cy="117.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="247.7" cy="145.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="145.3" cy="223.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="295.3" cy="98.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="172.2" cy="180.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="350.7" cy="92.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="210.5" cy="168.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="252.2" cy="144.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="236.2" cy="169.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="238.1" cy="199.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="426.6" cy="102.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="176.2" cy="173.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="376.1" cy="105.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="263.5" cy="135.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="177.2" cy="245.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="332.5" cy="134.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="288.7" cy="149.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="270.7" cy="89.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="157.0" cy="224.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="269.7" cy="167.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="212.3" cy="179.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="210.6" cy="138.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="219.5" cy="99.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="231.2" cy="205.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="374.1" cy="60.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="238.6" cy="210.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="116.2" cy="195.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="321.9" cy="81.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="252.4" cy="132.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="231.7" cy="227.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="71.5" cy="261.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="278.7" cy="101.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="190.4" cy="172.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="310.8" cy="102.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="278.9" cy="149.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="261.7" cy="129.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="197.2" cy="171.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="97.5" cy="251.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="313.5" cy="104.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="274.5" cy="85.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="223.5" cy="210.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="189.2" cy="215.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="193.9" cy="227.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="106.9" cy="255.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="147.4" cy="206.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="219.7" cy="156.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="329.4" cy="94.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="266.0" cy="144.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="354.3" cy="145.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="165.8" cy="209.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="363.7" cy="152.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="209.2" cy="186.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="346.3" cy="100.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="299.0" cy="121.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="231.7" cy="129.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="244.0" cy="159.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="330.2" cy="93.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="172.6" cy="113.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="83.7" cy="222.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="274.8" cy="182.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="411.4" cy="123.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="115.3" cy="240.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="228.2" cy="137.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="121.0" cy="221.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="200.5" cy="160.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="164.2" cy="217.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="280.7" cy="143.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="197.0" cy="195.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="233.0" cy="118.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="172.7" cy="179.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="306.3" cy="180.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="170.1" cy="189.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="170.1" cy="134.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="236.8" cy="166.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="114.5" cy="153.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="218.0" cy="160.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="97.3" cy="218.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="205.8" cy="183.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="226.9" cy="180.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="177.8" cy="186.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="193.9" cy="157.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="202.2" cy="157.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="280.9" cy="158.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="201.8" cy="150.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="165.1" cy="221.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="222.2" cy="172.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="198.4" cy="174.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="259.8" cy="174.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="221.1" cy="201.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="113.3" cy="214.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="346.2" cy="78.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="200.6" cy="148.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="175.6" cy="175.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="274.3" cy="104.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="87.5" cy="250.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="221.9" cy="165.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="259.2" cy="201.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="195.5" cy="177.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="235.7" cy="162.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="218.7" cy="121.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="211.5" cy="143.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="197.3" cy="133.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="261.5" cy="189.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="144.4" cy="215.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="276.3" cy="152.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="247.1" cy="193.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="171.4" cy="201.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="205.0" cy="166.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="219.0" cy="164.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="336.8" cy="151.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="301.3" cy="73.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="182.6" cy="184.1" r="2.6" fill-opacity=".45"/><circle class="dot" cx="166.9" cy="187.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="191.7" cy="224.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="249.8" cy="128.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="249.0" cy="181.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="241.0" cy="169.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="318.6" cy="141.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="232.5" cy="124.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="260.5" cy="207.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="258.8" cy="185.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="196.3" cy="173.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="232.2" cy="164.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="186.2" cy="163.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="227.2" cy="196.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="341.8" cy="101.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="291.2" cy="169.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="30.1" cy="285.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="184.8" cy="204.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="221.1" cy="187.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="224.3" cy="156.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="168.3" cy="198.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="190.8" cy="200.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="209.8" cy="218.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="202.7" cy="135.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="287.6" cy="175.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="248.8" cy="168.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="207.5" cy="231.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="216.8" cy="216.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="248.7" cy="162.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="154.3" cy="161.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="208.0" cy="144.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="272.9" cy="160.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="270.8" cy="159.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="48.4" cy="232.2" r="2.6" fill-opacity=".45"/><circle class="dot" cx="391.4" cy="41.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="178.5" cy="213.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="287.9" cy="159.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="136.3" cy="174.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="293.4" cy="167.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="217.1" cy="142.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="220.2" cy="191.6" r="2.6" fill-opacity=".45"/><circle class="dot" cx="224.6" cy="166.4" r="2.6" fill-opacity=".45"/><circle class="dot" cx="226.7" cy="215.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="309.6" cy="127.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="175.2" cy="225.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="255.8" cy="211.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="193.7" cy="197.3" r="2.6" fill-opacity=".45"/><circle class="dot" cx="88.9" cy="190.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="234.5" cy="154.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="207.0" cy="167.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="210.5" cy="162.7" r="2.6" fill-opacity=".45"/><circle class="dot" cx="133.0" cy="235.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="181.3" cy="147.9" r="2.6" fill-opacity=".45"/><circle class="dot" cx="224.8" cy="211.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="250.5" cy="109.5" r="2.6" fill-opacity=".45"/><circle class="dot" cx="226.5" cy="151.8" r="2.6" fill-opacity=".45"/><circle class="dot" cx="139.6" cy="205.0" r="2.6" fill-opacity=".45"/><circle class="dot" cx="293.5" cy="198.0" r="2.6" fill-opacity=".45"/><line class="curve2" x1="227.1" y1="170.0" x2="370.8" y2="92.6" stroke-width="3.5"/><polygon class="dot2" points="379.6,87.9 373.7,97.9 368.0,87.3"/><line class="curve4" x1="227.1" y1="170.0" x2="202.2" y2="123.6" stroke-width="3.5"/><polygon class="dot3" points="197.4,114.8 207.5,120.8 196.9,126.5"/></svg>
<figcaption>The purple points are the data. The orange arrow is the first component, the green the second; both start at the mean, their lengths are two standard deviations along that direction. Most of the spread is in the orange direction.</figcaption>
</figure>

## The same result with SVD

In practice PCA is usually computed without building the covariance matrix,
through the **singular value decomposition** (SVD) of the centred data. If
`Xc = U S Vᵀ`, the rows of `Vᵀ` are the components and `S² / (n − 1)` the
variances:

```python
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
print((S ** 2 / (len(X) - 1)).round(3))
print(np.allclose(np.abs(Vt), np.abs(vecs.T)))
```

```text
[5.107 0.531]
True
```

Since SVD never builds the covariance matrix, it is numerically more stable.

## How many components?

Let us look at real data: 8×8-pixel handwritten digits, so 64 features per
image. How much of the variance do how many components carry, and how much is
lost when we rebuild the image from few components?

```python
from sklearn.datasets import load_digits

D = load_digits().data                       # 1797 images, 64 pixels
p = PCA().fit(D)
cum = np.cumsum(p.explained_variance_ratio_)
for target in (0.5, 0.8, 0.9, 0.95, 0.99):
    print(target, int(np.searchsorted(cum, target) + 1))
for k in (2, 10, 20, 40):
    pk = PCA(k).fit(D)
    R = pk.inverse_transform(pk.transform(D))     # rebuild from k components
    print(k, round(float(cum[k - 1]), 3), round(float(((D - R) ** 2).mean()), 3))
```

```text
0.5 5
0.8 13
0.9 21
0.95 29
0.99 41
2 0.285 13.421
10 0.738 4.914
20 0.894 1.984
40 0.988 0.221
```

Half of the variance of the 64 pixels is in 5 components, 90% in 21, 99% in
41. With 20 components 89.4% of the variance remains and the mean squared
error per pixel is 1.984 (pixels range 0–16); with 40 components the error
drops to 0.221. A common rule is the smallest `k` that keeps 90% or 95% of the
variance; with `PCA(0.95)` scikit-learn picks it itself.

<figure class="fig">
<svg viewBox="0 0 480 230" width="480" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="200.0" x2="460" y2="200.0"/><text class="dim" x="38" y="204.0" font-size="11" text-anchor="end">0</text><line class="grid" x1="44" y1="155.0" x2="460" y2="155.0"/><text class="dim" x="38" y="159.0" font-size="11" text-anchor="end">0.25</text><line class="grid" x1="44" y1="110.0" x2="460" y2="110.0"/><text class="dim" x="38" y="114.0" font-size="11" text-anchor="end">0.5</text><line class="grid" x1="44" y1="65.0" x2="460" y2="65.0"/><text class="dim" x="38" y="69.0" font-size="11" text-anchor="end">0.75</text><line class="grid" x1="44" y1="20.0" x2="460" y2="20.0"/><text class="dim" x="38" y="24.0" font-size="11" text-anchor="end">1.0</text><text class="dim" x="44.0" y="220" font-size="11" text-anchor="middle">1</text><text class="dim" x="143.0" y="220" font-size="11" text-anchor="middle">16</text><text class="dim" x="248.7" y="220" font-size="11" text-anchor="middle">32</text><text class="dim" x="354.3" y="220" font-size="11" text-anchor="middle">48</text><text class="dim" x="460.0" y="220" font-size="11" text-anchor="middle">64</text><line class="curve2" x1="44" y1="38.0" x2="176.1" y2="38.0" stroke-dasharray="6 4"/><line class="curve2" x1="176.1" y1="38.0" x2="176.1" y2="200.0" stroke-dasharray="6 4"/><polyline class="curve" points="44.0,173.2 50.6,148.7 57.2,127.5 63.8,112.3 70.4,101.9 77.0,93.1 83.6,85.3 90.2,78.7 96.8,72.7 103.4,67.1 110.0,62.8 116.6,58.8 123.2,55.5 129.8,52.3 136.4,49.6 143.0,47.1 149.7,44.7 156.3,42.5 162.9,40.7 169.5,39.0 176.1,37.4 182.7,36.0 189.3,34.6 195.9,33.3 202.5,32.1 209.1,31.0 215.7,29.9 222.3,29.0 228.9,28.1 235.5,27.4 242.1,26.7 248.7,26.1 255.3,25.5 261.9,24.9 268.5,24.3 275.1,23.8 281.7,23.3 288.3,22.9 294.9,22.5 301.5,22.1 308.1,21.8 314.7,21.5 321.3,21.2 327.9,21.0 334.5,20.8 341.1,20.6 347.7,20.4 354.3,20.3 361.0,20.2 367.6,20.1 374.2,20.0 380.8,20.0 387.4,20.0 394.0,20.0 400.6,20.0 407.2,20.0 413.8,20.0 420.4,20.0 427.0,20.0 433.6,20.0 440.2,20.0 446.8,20.0 453.4,20.0 460.0,20.0"/></svg>
<figcaption>Cumulative explained variance by number of components on the digit data. Orange dashed line: 90% is reached at 21 components.</figcaption>
</figure>

## Scale changes everything

PCA looks at variance; a feature with a large unit has a large variance too.
In the wine data (13 chemical measurements) the features' standard deviations
are very different:

```python
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

wine = load_wine()
W, names = wine.data, wine.feature_names
print(W.std(axis=0).round(1)[[0, 4, 12]])
for name, data in (("raw", W), ("scaled", StandardScaler().fit_transform(W))):
    pw = PCA(2).fit(data)
    top = np.argmax(np.abs(pw.components_[0]))
    print(name, pw.explained_variance_ratio_.round(3), names[top])
```

```text
[  0.8  14.2 314. ]
raw [0.998 0.002] proline
scaled [0.362 0.192] flavanoids
```

Alcohol's standard deviation is 0.8, magnesium's 14.2, proline's 314. On raw
data the first component "explains" 99.8% of the variance, but this is an
illusion: that component is almost only proline; PCA has merely found the
column with the largest unit. After standardising, the first two components
take 36.2% and 19.2%, and the heaviest feature in the first component is the
flavanoids. If features are in different units, standardise before PCA.

## Summary

- PCA rotates the data onto perpendicular directions of greatest spread.
- The components are the covariance matrix's eigenvectors, their variances
  the eigenvalues; in practice computed with SVD.
- The new axes are uncorrelated; the explained variance ratio is each axis's
  share.
- `k` is chosen to keep 90–95% of the variance; the loss of rebuilding from
  few components can be measured.
- The components' signs are arbitrary; if the units differ, standardise
  first.
