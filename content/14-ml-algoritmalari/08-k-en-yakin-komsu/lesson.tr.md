# K En Yakın Komşu

**K en yakın komşu (k-nearest neighbours, KNN)** belki de en sezgisel model:
yeni bir örneğin sınıfını, ona en yakın `k` eğitim örneğinin oyuyla belirler.
"Öğrenme" yoktur; model eğitim verisini olduğu gibi saklar ve bütün iş tahmin
anında yapılır. Bu yüzden basit ama tahmini pahalı, ve iki zayıf yanı var:
ölçek ve boyut.

## Komşuları bulmak ve oylamak

İç içe geçmiş iki yay biçiminde, doğrusal bir sınırla ayrılamayan bir veri:

```python
import numpy as np

rng = np.random.default_rng(8)


def moons(n, noise):
    t = rng.uniform(0, np.pi, n)
    y = rng.integers(0, 2, n)
    x = np.where(y == 0, np.cos(t), 1 - np.cos(t))
    z = np.where(y == 0, np.sin(t), 0.5 - np.sin(t))
    return np.column_stack([x, z]) + rng.normal(0, noise, (n, 2)), y


X, y = moons(300, 0.25)                                # eğitim
Xt, yt = moons(500, 0.25)                              # test


def knn_predict(Xtr, ytr, Xq, k):
    # bütün uzaklıklar
    d = ((Xq[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    near = np.argsort(d, axis=1)[:, :k]                # en yakın k'nın yeri
    votes = ytr[near]
    return np.array([np.bincount(v, minlength=2).argmax() for v in votes])


from sklearn.neighbors import KNeighborsClassifier

ours = knn_predict(X, y, Xt, 5)
ref = KNeighborsClassifier(n_neighbors=5).fit(X, y).predict(Xt)
print((ours == ref).mean(), round((ours == yt).mean(), 3))
```

```text
1.0 0.934
```

<figure class="fig">
<svg viewBox="0 0 560 330" width="560" xmlns="http://www.w3.org/2000/svg"><circle class="dot" cx="255.5" cy="113.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="448.0" cy="128.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="323.0" cy="257.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="87.7" cy="91.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="444.3" cy="209.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="295.7" cy="88.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="296.4" cy="271.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="255.0" cy="243.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="293.9" cy="82.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="331.2" cy="263.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="272.9" cy="105.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="321.6" cy="102.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="274.7" cy="137.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="255.7" cy="85.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="128.8" cy="124.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="245.8" cy="97.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="240.6" cy="194.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="360.8" cy="234.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="176.3" cy="76.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="164.4" cy="58.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="84.2" cy="143.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="291.6" cy="159.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="234.1" cy="60.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="244.3" cy="193.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="297.9" cy="178.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="275.0" cy="97.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="268.9" cy="236.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="268.6" cy="272.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="172.9" cy="135.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="190.9" cy="32.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="144.4" cy="58.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="211.2" cy="262.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="206.7" cy="159.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="266.5" cy="248.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="348.8" cy="183.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="279.3" cy="77.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="192.6" cy="49.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="165.9" cy="111.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="441.6" cy="193.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="293.0" cy="153.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="59.0" cy="164.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="115.5" cy="135.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="106.4" cy="185.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="375.0" cy="155.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="258.3" cy="82.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="321.2" cy="217.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="457.1" cy="202.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="230.6" cy="222.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="311.0" cy="268.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="204.0" cy="201.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="263.2" cy="69.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="345.6" cy="204.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="241.9" cy="72.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="314.4" cy="211.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="299.7" cy="93.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="144.8" cy="116.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="228.2" cy="179.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="170.1" cy="71.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="315.6" cy="299.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="235.7" cy="201.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="284.4" cy="98.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="166.5" cy="169.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="225.7" cy="264.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="253.0" cy="87.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="314.1" cy="241.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="311.4" cy="220.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="433.1" cy="226.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="284.5" cy="252.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="268.2" cy="129.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="34.2" cy="174.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="344.1" cy="207.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="90.0" cy="94.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="330.4" cy="263.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="225.7" cy="210.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="335.7" cy="196.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="328.5" cy="144.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="235.7" cy="303.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="164.6" cy="206.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="177.0" cy="116.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="426.7" cy="154.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="390.0" cy="264.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="250.6" cy="108.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="222.3" cy="214.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="147.5" cy="87.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="432.6" cy="162.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="133.1" cy="48.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="271.8" cy="50.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="161.0" cy="76.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="323.8" cy="144.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="245.4" cy="24.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="435.2" cy="157.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="213.7" cy="250.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="193.9" cy="58.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="164.9" cy="134.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="451.7" cy="142.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="171.2" cy="56.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="259.4" cy="287.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="116.8" cy="89.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="291.5" cy="249.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="220.8" cy="151.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="414.9" cy="176.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="308.9" cy="206.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="130.1" cy="185.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="289.0" cy="77.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="299.4" cy="159.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="318.9" cy="293.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="451.9" cy="220.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="54.9" cy="202.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="133.6" cy="119.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="207.7" cy="140.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="141.6" cy="66.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="204.3" cy="89.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="182.1" cy="245.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="83.6" cy="105.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="155.2" cy="110.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="96.4" cy="128.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="248.5" cy="76.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="131.1" cy="117.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="381.8" cy="221.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="305.9" cy="185.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="410.1" cy="244.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="432.4" cy="106.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="206.1" cy="127.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="342.2" cy="140.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="231.6" cy="111.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="263.3" cy="149.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="281.6" cy="308.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="328.7" cy="245.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="390.4" cy="265.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="138.6" cy="87.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="86.0" cy="217.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="126.3" cy="135.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="241.5" cy="97.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="183.2" cy="139.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="59.7" cy="145.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="209.7" cy="81.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="247.3" cy="168.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="226.5" cy="245.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="399.1" cy="131.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="293.2" cy="274.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="403.9" cy="192.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="295.6" cy="273.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="327.4" cy="220.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="255.9" cy="306.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="420.4" cy="198.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="359.5" cy="273.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="451.2" cy="199.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="438.4" cy="253.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="103.2" cy="187.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="219.3" cy="115.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="297.3" cy="264.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="101.4" cy="101.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="137.7" cy="79.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="227.9" cy="97.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="304.2" cy="122.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="234.1" cy="208.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="30.7" cy="210.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="270.6" cy="70.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="278.9" cy="90.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="362.7" cy="255.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="307.7" cy="210.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="221.8" cy="139.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="133.0" cy="118.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="352.5" cy="274.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="301.4" cy="118.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="498.7" cy="164.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="348.1" cy="111.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="147.2" cy="151.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="155.0" cy="161.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="230.9" cy="145.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="221.0" cy="200.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="407.3" cy="298.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="292.6" cy="143.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="227.1" cy="220.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="133.9" cy="142.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="185.6" cy="76.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="59.0" cy="166.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="32.8" cy="242.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="114.4" cy="82.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="175.3" cy="161.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="143.8" cy="81.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="241.3" cy="227.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="177.1" cy="185.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="320.2" cy="241.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="175.1" cy="141.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="92.0" cy="143.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="287.9" cy="287.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="360.8" cy="270.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="411.9" cy="169.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="133.5" cy="79.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="69.8" cy="159.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="125.6" cy="73.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="92.8" cy="194.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="377.1" cy="228.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="266.5" cy="54.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="198.7" cy="191.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="81.8" cy="151.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="183.0" cy="117.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="299.7" cy="208.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="335.6" cy="143.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="49.8" cy="139.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="148.0" cy="25.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="162.2" cy="127.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="301.5" cy="187.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="250.4" cy="197.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="352.6" cy="244.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="260.4" cy="241.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="396.3" cy="228.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="434.1" cy="153.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="375.0" cy="233.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="234.5" cy="70.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="74.8" cy="199.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="219.6" cy="251.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="393.2" cy="205.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="202.5" cy="184.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="202.9" cy="233.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="143.2" cy="125.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="69.3" cy="127.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="238.1" cy="78.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="266.5" cy="274.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="401.2" cy="256.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="401.0" cy="250.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="149.3" cy="133.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="137.1" cy="135.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="331.0" cy="163.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="318.9" cy="116.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="419.4" cy="235.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="137.2" cy="170.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="90.7" cy="224.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="231.2" cy="92.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="438.4" cy="255.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="145.7" cy="45.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="188.1" cy="173.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="126.1" cy="141.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="239.5" cy="48.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="188.7" cy="128.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="292.2" cy="161.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="234.6" cy="177.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="201.9" cy="184.1" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="437.8" cy="169.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="313.4" cy="287.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="210.1" cy="69.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="206.2" cy="99.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="115.1" cy="208.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="205.9" cy="88.0" r="3.2" fill-opacity=".8"/><circle class="dot" cx="228.5" cy="70.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="272.3" cy="28.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="286.5" cy="108.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="163.0" cy="145.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="99.1" cy="197.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="227.8" cy="196.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="312.3" cy="157.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="91.5" cy="137.0" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="395.1" cy="250.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="10.6" cy="187.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="270.5" cy="274.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="229.1" cy="255.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="457.7" cy="158.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="334.6" cy="191.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="426.7" cy="253.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="397.2" cy="199.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="409.6" cy="205.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="309.2" cy="227.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="212.9" cy="235.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="302.7" cy="239.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="318.5" cy="322.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="59.6" cy="161.1" r="3.2" fill-opacity=".8"/><circle class="dot" cx="260.6" cy="163.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="160.7" cy="31.8" r="3.2" fill-opacity=".8"/><circle class="dot" cx="302.9" cy="92.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="373.6" cy="314.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="436.1" cy="207.4" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="263.4" cy="271.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="304.3" cy="278.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="213.2" cy="206.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="310.7" cy="113.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="350.2" cy="203.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="280.9" cy="307.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="135.7" cy="160.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="153.8" cy="81.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="410.5" cy="230.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="252.1" cy="227.6" r="3.2" fill-opacity=".8"/><circle class="dot" cx="216.0" cy="47.4" r="3.2" fill-opacity=".8"/><circle class="dot" cx="174.0" cy="124.3" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="178.1" cy="153.2" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="475.4" cy="212.3" r="3.2" fill-opacity=".8"/><circle class="dot" cx="280.3" cy="98.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="261.7" cy="82.2" r="3.2" fill-opacity=".8"/><circle class="dot" cx="314.4" cy="168.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="204.6" cy="84.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="428.6" cy="224.8" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="270.1" cy="246.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="159.9" cy="100.9" r="3.2" fill-opacity=".8"/><circle class="dot" cx="131.1" cy="79.7" r="3.2" fill-opacity=".8"/><circle class="dot" cx="106.6" cy="184.5" r="3.2" fill-opacity=".8"/><circle class="dot" cx="70.8" cy="131.5" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="326.1" cy="307.9" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="292.1" cy="216.6" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="419.2" cy="204.7" r="3.2" fill-opacity=".8"/><circle class="dot2" cx="332.7" cy="275.1" r="3.2" fill-opacity=".8"/><circle class="curve3" cx="265.0" cy="170.0" r="38.5" fill="none"/><circle class="dot3" cx="265.0" cy="170.0" r="6"/></svg>
<figcaption>Eğitim verisi: sınıf 0 mor, sınıf 1 turuncu. Yeşil sorgu noktasının çemberi en yakın 15 komşuyu içine alıyor: 8 mor, 7 turuncu; tahmin mor.</figcaption>
</figure>

500 test örneğinin hepsinde scikit-learn ile aynı tahmin; doğruluk 0,934.
Uzaklıkları yayınla tek seferde hesapladık: `(500, 1, 2) − (1, 300, 2)` →
`(500, 300)` uzaklık matrisi. Uzaklığın karekökünü almadık: sıralamayı
değiştirmez.

## k'yı seçmek

```python
for k in (1, 5, 15, 51, 151):
    tr = (knn_predict(X, y, X, k) == y).mean()
    te = (knn_predict(X, y, Xt, k) == yt).mean()
    print(k, round(tr, 3), round(te, 3))
```

```text
1 1.0 0.91
5 0.95 0.934
15 0.947 0.938
51 0.93 0.936
151 0.847 0.85
```

`k = 1` eğitimde kusursuz (her nokta kendisinin en yakın komşusu) ama testte
0,91: gürültüyü ezberliyor, **aşırı uyum**. `k = 15` testte en iyisi (0,938).
`k = 151` eğitim verisinin yarısına bakıyor ve iki yayı ayıramıyor: **eksik
uyum** (0,85). Küçük `k` karmaşık, büyük `k` düz bir sınır çizer; `k` yine
çapraz doğrulamayla seçilir.

## Ölçek her şeyi değiştirir

KNN uzaklığa dayandığı için büyük ölçekli bir özellik ötekileri ezer. İkinci
özelliği bin ile çarpalım (örneğin metre yerine milimetre):

```python
Xs, Xts = X * [1, 1000], Xt * [1, 1000]
print(round((knn_predict(Xs, y, Xts, 15) == yt).mean(), 3))
mu, sd = Xs.mean(axis=0), Xs.std(axis=0)
Zs, Zts = (Xs - mu) / sd, (Xts - mu) / sd
print(round((knn_predict(Zs, y, Zts, 15) == yt).mean(), 3))
```

```text
0.818
0.944
```

Doğruluk 0,938'den 0,818'e düştü: uzaklık artık neredeyse yalnızca ikinci
özellikten oluşuyor. Standartlaştırınca 0,944'e döndü. Bilgi aynı, birim
farklı; KNN'den önce standartlaştırma şart.

## Boyut laneti

Boyut sayısı arttıkça "en yakın" ile "en uzak" arasındaki fark erir. Birim
küpte 500 rastgele nokta ve bir sorgu noktası:

```python
for d in (2, 10, 100, 1000):
    P = rng.random((500, d))
    q = rng.random(d)
    dist = np.sqrt(((P - q) ** 2).sum(axis=1))
    print(d, round(dist.min() / dist.max(), 3))
```

```text
2 0.027
10 0.261
100 0.752
1000 0.889
```

İki boyutta en yakın nokta en uzağın %3'ü kadar uzakta; bin boyutta %89'u.
Herkes herkese neredeyse eşit uzaklıktaysa "en yakın komşu" anlamını
yitirir. Buna **boyut laneti (curse of dimensionality)** denir; çok özellikli
veride KNN'den önce boyut azaltma (bölüm 17, PCA) ya da özellik seçimi
yapılır.

## Özet

- KNN eğitimde bir şey öğrenmez; tahminde en yakın `k` örneğin oyuna bakar.
- Uzaklık matrisi yayınla tek seferde: `(q, 1, d) − (1, n, d)`.
- Küçük `k` aşırı, büyük `k` eksik uyum; çapraz doğrulamayla seç.
- Uzaklığa dayalı her yöntemde olduğu gibi önce standartlaştır.
- Boyut arttıkça uzaklıklar birbirine yaklaşır; çok boyutta KNN zayıflar.
