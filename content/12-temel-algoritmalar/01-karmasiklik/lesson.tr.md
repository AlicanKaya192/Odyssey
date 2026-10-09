# Karmaşıklık ve Büyük O

Önceki bölümde aynı problemi çözen iki algoritma gördük: biri `n` toplama
yapıyordu, öbürü her zaman birkaç işlem. İkisi de doğruydu; fark, **girdi
büyüdükçe yapılan işin nasıl büyüdüğündeydi**. Bu bölümde o farkı ölçmeyi
ve tek bir gösterimle söylemeyi öğreneceğiz: **Büyük O (Big O)**.

## Neden saniye değil?

Bir algoritmanın kaç saniye sürdüğünü ölçebiliriz ama bu sayı pek bir şey
söylemez: aynı kod hızlı bir bilgisayarda kısa, eski bir bilgisayarda uzun
sürer; arka planda başka bir program çalışıyorsa yine değişir. Bunun yerine
algoritmanın **kaç adım attığını** sayarız. Adım derken kabaca tek bir
basit işlemi kastediyoruz: bir karşılaştırma, bir toplama, bir atama.

Adım saymanın en kolay yolu algoritmaya bir sayaç eklemek. Listede bir
değeri baştan sona arayan **doğrusal arama (linear search)** için:

```python
def linear_search(items, target):
    steps = 0
    for i in range(len(items)):
        steps += 1
        if items[i] == target:
            return i, steps
    return -1, steps

data = list(range(1, 1001))
print(linear_search(data, 1))
print(linear_search(data, 500))
print(linear_search(data, 1000))
print(linear_search(data, 5000))
```

```text
(0, 1)
(499, 500)
(999, 1000)
(-1, 1000)
```

Aynı fonksiyon, aynı liste: aranan baştaysa **1** adım, sondaysa ya da hiç
yoksa **1000** adım. Buradan iki önemli fikir çıkıyor.

## En iyi, ortalama ve en kötü durum

- **En iyi durum (best case):** aranan ilk eleman, 1 adım.
- **En kötü durum (worst case):** aranan son eleman ya da yok, `n` adım.
- **Ortalama durum (average case):** rastgele bir yerde, yaklaşık `n / 2`.

Algoritmaları karşılaştırırken çoğunlukla **en kötü duruma** bakarız:
"ne olursa olsun bundan fazla sürmez" diyebilmek isteriz. Bir uygulamada
en iyi duruma güvenmek, kötü günde sistemin kilitlenmesi demektir.

## Büyüme: adım sayısı `n` ile nasıl artıyor?

Bir algoritmanın adım sayısını girdinin büyüklüğü `n`'ye bağlı bir ifade
olarak yazabiliriz. Doğrusal arama en kötü durumda `n` adım atıyor. Peki
şu iç içe döngü?

```python
def count_pairs(n):
    steps = 0
    for i in range(n):
        for j in range(i + 1, n):
            steps += 1
    return steps

for n in [10, 100, 1000, 2000]:
    print(n, count_pairs(n))
```

```text
10 45
100 4950
1000 499500
2000 1999000
```

Bu döngü listedeki **her ikiliyi** bir kez geziyor: `n × (n − 1) / 2` adım.
`n` 1000'den 2000'e iki katına çıkınca adım sayısı **dört katına** çıktı
(499 500 → 1 999 000). Doğrusal aramada iki kat girdi iki kat iş demekti;
burada dört kat. İşte "büyüme hızı" dediğimiz şey bu.

Bir de her turda sayıyı yarıya bölen bir döngüye bakalım:

```python
def halving_steps(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps

for n in [10, 100, 1000, 1_000_000, 1_000_000_000]:
    print(n, halving_steps(n))
```

```text
10 3
100 6
1000 9
1000000 19
1000000000 29
```

Bir milyardan 1'e inmek için yalnızca **29** yarıya bölme yetiyor. Girdi
bin kat büyüyünce adım sayısı yalnızca 10 kadar arttı. "Kaç kez ikiye
bölebilirim?" sorusunun cevabına **logaritma** denir: `log₂ n`. İkili arama
(bir sonraki bölümlerde) tam olarak bu sayede bu kadar hızlı.

## Büyük O gösterimi

Adım sayısını tam olarak yazmak (`3n + 5`, `n²/2 − n/2` gibi) gereksiz
ayrıntı verir. Büyük O yalnızca **baskın terimi** tutar, iki kuralla:

1. **Sabit çarpanlar atılır:** `3n` → `O(n)`, `n²/2` → `O(n²)`.
2. **Küçük terimler atılır:** `n² + n + 7` → `O(n²)`.

Neden atabiliyoruz? Çünkü `n` büyüdükçe baskın terim her şeyi ezer. `n`
bir milyon iken `n²` bir trilyon, `n` ise yalnızca bir milyon: ikincisi
birincinin milyonda biri. Sabitler de bilgisayarın hızı gibi algoritma
dışındaki şeylere bağlıdır; Büyük O onları bilerek görmezden gelir.

Sık karşılaşacağın sınıflar, hızlıdan yavaşa:

| Gösterim | Adı | Örnek | n = 1 000 000 için adım |
|---|---|---|---|
| `O(1)` | sabit (constant) | listede `items[5]`, formülle toplam | 1 |
| `O(log n)` | logaritmik | ikili arama, yarıya bölme | ~20 |
| `O(n)` | doğrusal (linear) | doğrusal arama, en büyüğü bulma | 1 000 000 |
| `O(n log n)` | n log n | verimli sıralamalar (merge sort) | ~20 000 000 |
| `O(n²)` | karesel (quadratic) | her ikiliyi gezmek | 1 000 000 000 000 |
| `O(2ⁿ)` | üstel (exponential) | bütün alt kümeleri denemek | hesaplanamayacak kadar çok |

Bu sayıları gerçek bir süreye çevirelim. Bu bilgisayarda basit bir Python
döngüsü saniyede yaklaşık **10 milyon** adım atıyor (ölçüldü). O
zaman bir milyon elemanlık girdide `O(n)` bir algoritma saniyenin onda biri,
`O(n log n)` birkaç saniye, `O(n²)` ise saatlerce sürer. Aradaki fark
bilgisayar alarak kapatılamaz; algoritma değiştirerek kapatılır.

## Büyük O'yu koda bakarak bulmak

Çoğu zaman sayaç eklemene gerek kalmaz; koda bakıp şu kurallarla
tahmin edersin:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Tek bir basit işlem</span><span><code>O(1)</code>: atama, karşılaştırma, <code>items[i]</code>.</span></div>
    <div class="anat-row"><span>Bir döngü, içi sabit</span><span><code>O(n)</code>: döngü <code>n</code> kez döner.</span></div>
    <div class="anat-row"><span>İç içe döngüler</span><span><b>Çarpılır</b>: <code>n</code> × <code>n</code> = <code>O(n²)</code>.</span></div>
    <div class="anat-row"><span>Art arda bloklar</span><span><b>Toplanır</b>, en büyüğü kalır: <code>O(n) + O(n²)</code> = <code>O(n²)</code>.</span></div>
    <div class="anat-row"><span>Her turda yarıya bölen döngü</span><span><code>O(log n)</code>.</span></div>
    <div class="anat-row"><span>Hazır fonksiyon çağrısı</span><span>İçindeki döngüyü say: <code>max</code>, <code>sum</code>, <code>in</code> (listede) <code>O(n)</code>.</span></div>
  </div>
  <figcaption>Koda bakarak Büyük O tahmini. Hazır fonksiyonlar tek satır olsa da içlerinde döngü olabilir.</figcaption>
</figure>

Örnek: önce listeyi bir kez gezen (`O(n)`), sonra her ikiliye bakan
(`O(n²)`) bir fonksiyon toplamda `O(n + n²) = O(n²)`.

## Bellek de bir maliyet

Büyük O yalnızca süre için değil, **ek bellek** için de kullanılır. En büyük
sayıyı bulan döngü yalnızca tek bir değişken tutar: `O(1)` ek bellek.
Listenin her elemanının karesini yeni bir listeye yazan kod ise `n` elemanlık
yeni bir liste kurar: `O(n)` ek bellek. Bazen hız için bellek harcarız (bir
sonraki bölümlerde kümeyle tekrar bulmak gibi); bu bilinçli bir takastır.

## Özet

- Algoritmalar saniyeyle değil, **girdi büyüdükçe adım sayısının nasıl
  büyüdüğüyle** karşılaştırılır.
- Genelde **en kötü duruma** bakılır.
- Büyük O baskın terimi tutar; sabitler ve küçük terimler atılır.
- Sınıflar: `O(1)` < `O(log n)` < `O(n)` < `O(n log n)` < `O(n²)` < `O(2ⁿ)`.
- İç içe döngüler çarpılır, art arda bloklar toplanır (en büyüğü kalır),
  her turda yarıya bölen döngü `O(log n)`.
- Ek bellek de Büyük O ile söylenir.
