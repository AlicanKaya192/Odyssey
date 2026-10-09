# Geri İzleme

Bir labirentte çıkışı arıyorsun. Bir kavşağa gelince yollardan birini
seçersin; çıkmaz sokağa girersen **son kavşağa geri dönüp** başka yolu
denersin. **Geri izleme (backtracking)** tam olarak bu: bir çözümü adım adım
kur, her adımda bir seçim yap, seçim bir yere çıkmıyorsa geri al ve sıradaki
seçimi dene.

Bütün olasılıkları denemek gereken problemler için kullanılır: bir kümenin
bütün alt kümeleri, bir listenin bütün sıralanışları, kurallara uyan
yerleşimler (sudoku, satranç bulmacaları), toplamı hedefi tutan seçimler.
Asıl gücü **budama**: bir seçimin işe yaramayacağı anlaşıldığı an onun
altındaki bütün olasılıkları hiç denemeden atmak.

## İskelet: seç, keşfet, geri al

```python
def backtrack(path):
    if TAMAM_MI(path):
        SONUCA_EKLE(path)
        return
    for choice in SECENEKLER(path):
        path.append(choice)        # seç
        backtrack(path)            # bu seçimle devam et
        path.pop()                 # geri al
```

Bütün geri izleme algoritmaları bu üç satırın çeşitlemesi. Önemli olan
`pop`: seçimi geri almazsan bir sonraki deneme öncekinin artığıyla başlar.

## Bütün alt kümeler

`[1, 2, 3]`'ün alt kümeleri: her eleman ya var ya yok. Her adımda "sıradaki
elemanlardan hangisini ekleyeyim?" diye sorarız:

```python
def subsets(items):
    result, path = [], []
    def backtrack(start):
        result.append(path[:])            # her düğüm bir alt küme
        for i in range(start, len(items)):
            path.append(items[i])
            backtrack(i + 1)              # sonraki elemanlardan devam
            path.pop()
    backtrack(0)
    return result

print(subsets([1, 2, 3]))
print(len(subsets(list(range(20)))))
```

```text
[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
1048576
```

<figure class="fig">
<svg viewBox="0 0 317 222" width="317" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="47.9" y1="140.0" x2="47.9" y2="200.0"/>
<line class="line" x1="84.9" y1="80.0" x2="47.9" y2="140.0"/>
<line class="line" x1="84.9" y1="80.0" x2="121.9" y2="140.0"/>
<line class="line" x1="183.6" y1="20.0" x2="84.9" y2="80.0"/>
<line class="line" x1="195.9" y1="80.0" x2="195.9" y2="140.0"/>
<line class="line" x1="183.6" y1="20.0" x2="195.9" y2="80.0"/>
<line class="line" x1="183.6" y1="20.0" x2="269.9" y2="80.0"/>
<rect class="box" x="164.3" y="6.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="183.6" y="24.6" font-size="13" text-anchor="middle">[ ]</text>
<rect class="box" x="65.6" y="66.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="84.9" y="84.5" font-size="13" text-anchor="middle">[1]</text>
<rect class="box" x="17.3" y="126.0" width="61.2" height="28" rx="7"/>
<text class="ink" x="47.9" y="144.6" font-size="13" text-anchor="middle">[1, 2]</text>
<rect class="box" x="6.0" y="186.0" width="83.9" height="28" rx="7"/>
<text class="ink" x="47.9" y="204.6" font-size="13" text-anchor="middle">[1, 2, 3]</text>
<rect class="box" x="91.3" y="126.0" width="61.2" height="28" rx="7"/>
<text class="ink" x="121.9" y="144.6" font-size="13" text-anchor="middle">[1, 3]</text>
<rect class="box" x="176.6" y="66.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="195.9" y="84.5" font-size="13" text-anchor="middle">[2]</text>
<rect class="box" x="165.3" y="126.0" width="61.2" height="28" rx="7"/>
<text class="ink" x="195.9" y="144.6" font-size="13" text-anchor="middle">[2, 3]</text>
<rect class="box" x="250.6" y="66.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="269.9" y="84.5" font-size="13" text-anchor="middle">[3]</text>
</svg>
<figcaption>Her düğüm bir alt küme. Geri izleme ağacı soldan sağa, derinlemesine gezer; çıktıdaki sıra bu gezinmenin sırası.</figcaption>
</figure>

`path[:]` ile kopya ekliyoruz; `path`'in kendisini ekleseydik hepsi aynı
listeye bakar, sonunda hepsi boş kalırdı. `n` elemanın `2ⁿ` alt kümesi var:
20 elemanda bir milyonu geçti. Her eleman bir kat daha ekliyor; geri izleme
hızlı bir yöntem değil, **eksiksiz** bir yöntem.

## Bütün sıralanışlar (permütasyonlar)

Bu kez her adımda "henüz kullanılmamış elemanlardan hangisi?" diye
sorarız. Kullanılanları bir işaret listesinde tutarız:

```python
def permutations(items):
    result, path, used = [], [], [False] * len(items)
    def backtrack():
        if len(path) == len(items):
            result.append("".join(path))
            return
        for i, x in enumerate(items):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            backtrack()
            path.pop()
            used[i] = False           # geri alırken işareti de kaldır
    backtrack()
    return result

print(permutations("abc"))
```

```text
['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
```

`n` elemanın `n!` sıralanışı var: 10 elemanda 3 628 800. Hazırları
`itertools.permutations`, `itertools.combinations` ve
`itertools.product`; gerçek kodda onlar, ama kendi kuralını eklemen gerektiğinde
(budama) iskeleti kendin yazarsın.

## Budama: işe yaramayacak dalı hiç açma

Toplamı tam 50 olan alt kümeleri arayalım. Değerler pozitif ve sıralıysa
bir kural var: toplam 50'yi geçtiği an **o dalın altındaki hiçbir seçim**
işe yaramaz, daha büyük sayılar eklenecek. O dalı kesip atarız:

```python
def subset_sum(values, target, prune):
    values = sorted(values)
    found, path, nodes = [], [], [0]
    def backtrack(start, total):
        nodes[0] += 1
        if total == target:
            found.append(path[:])
        for i in range(start, len(values)):
            if prune and total + values[i] > target:
                break                     # sonrakiler daha da büyük
            path.append(values[i])
            backtrack(i + 1, total + values[i])
            path.pop()
    backtrack(0, 0)
    return len(found), nodes[0]
```

1 ile 59 arasından seçilmiş 20 farklı sayıda, budamasız ve budamalı
hâlinin ziyaret ettiği düğüm sayısı:

```text
without pruning : 11 solutions, 1048576 nodes
with pruning    : 11 solutions, 215 nodes
```

Aynı 11 çözüm; budamasız yöntem bütün `2²⁰` alt kümeyi geziyor, budamalı
yalnızca birkaç yüz düğüme uğruyor. Geri izlemenin bütün hüneri bu: iyi bir
budama kuralı.

## Sekiz vezir

Satranç tahtasına sekiz vezir, hiçbiri öbürünü tehdit etmeyecek şekilde
nasıl dizilir? Her satıra bir vezir koyarız; bir sütun ya da çapraz
doluysa o kareyi hiç denemeyiz.

```python
def queens(n):
    cols, diag1, diag2 = set(), set(), set()
    solutions, nodes = [0], [0]
    def place(row):
        nodes[0] += 1
        if row == n:
            solutions[0] += 1
            return
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue                  # tehdit altında: budama
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            place(row + 1)
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)
    place(0)
    return solutions[0], nodes[0]

print(queens(8))
```

```text
(92, 2057)
```

<figure class="fig">
<svg viewBox="0 0 274 274" width="274" xmlns="http://www.w3.org/2000/svg">
<rect class="box" x="35" y="1" width="34" height="34"/>
<rect class="box" x="103" y="1" width="34" height="34"/>
<rect class="box" x="171" y="1" width="34" height="34"/>
<rect class="box" x="239" y="1" width="34" height="34"/>
<rect class="box" x="1" y="35" width="34" height="34"/>
<rect class="box" x="69" y="35" width="34" height="34"/>
<rect class="box" x="137" y="35" width="34" height="34"/>
<rect class="box" x="205" y="35" width="34" height="34"/>
<rect class="box" x="35" y="69" width="34" height="34"/>
<rect class="box" x="103" y="69" width="34" height="34"/>
<rect class="box" x="171" y="69" width="34" height="34"/>
<rect class="box" x="239" y="69" width="34" height="34"/>
<rect class="box" x="1" y="103" width="34" height="34"/>
<rect class="box" x="69" y="103" width="34" height="34"/>
<rect class="box" x="137" y="103" width="34" height="34"/>
<rect class="box" x="205" y="103" width="34" height="34"/>
<rect class="box" x="35" y="137" width="34" height="34"/>
<rect class="box" x="103" y="137" width="34" height="34"/>
<rect class="box" x="171" y="137" width="34" height="34"/>
<rect class="box" x="239" y="137" width="34" height="34"/>
<rect class="box" x="1" y="171" width="34" height="34"/>
<rect class="box" x="69" y="171" width="34" height="34"/>
<rect class="box" x="137" y="171" width="34" height="34"/>
<rect class="box" x="205" y="171" width="34" height="34"/>
<rect class="box" x="35" y="205" width="34" height="34"/>
<rect class="box" x="103" y="205" width="34" height="34"/>
<rect class="box" x="171" y="205" width="34" height="34"/>
<rect class="box" x="239" y="205" width="34" height="34"/>
<rect class="box" x="1" y="239" width="34" height="34"/>
<rect class="box" x="69" y="239" width="34" height="34"/>
<rect class="box" x="137" y="239" width="34" height="34"/>
<rect class="box" x="205" y="239" width="34" height="34"/>
<rect class="line" x="1" y="1" width="272" height="272"/>
<circle class="dot" cx="18.0" cy="18.0" r="10.9"/>
<circle class="dot" cx="154.0" cy="52.0" r="10.9"/>
<circle class="dot" cx="256.0" cy="86.0" r="10.9"/>
<circle class="dot" cx="188.0" cy="120.0" r="10.9"/>
<circle class="dot" cx="86.0" cy="154.0" r="10.9"/>
<circle class="dot" cx="222.0" cy="188.0" r="10.9"/>
<circle class="dot" cx="52.0" cy="222.0" r="10.9"/>
<circle class="dot" cx="120.0" cy="256.0" r="10.9"/>
</svg>
<figcaption>Bulunan ilk çözüm: her satırda, her sütunda ve her çaprazda tek vezir.</figcaption>
</figure>

92 çözüm, yalnızca 2057 düğüm. Sekiz veziri 64 kareye satır başına birer
tane rastgele koymanın `8⁸ = 16 777 216` yolu var; her satıra ve sütuna bir
tane koyan permütasyonlar bile `8! = 40 320`. Kümeler (`set`) tehdit
denetimini `O(1)`'e indiriyor: aynı çaprazdaki karelerde `satır − sütun` ya
da `satır + sütun` sabit.

## Veri biliminde: neden "hepsini dene" ölçeklenmiyor

- **Özellik seçimi:** 30 özellikten en iyi alt kümeyi bulmak için bütün
  alt kümeleri denemek `2³⁰` = 1 073 741 824 model eğitmek demek. Bu yüzden
  pratikte açgözlü yöntemler (bir sonraki bölüm: ileri seçim) ya da
  düzenlileştirme (Lasso) kullanılır.
- **Hiperparametre ızgara araması:** scikit-learn'ün `GridSearchCV`'si
  `itertools.product` gibi bütün kombinasyonları dener; 4 parametre × 5
  değer = 625 kombinasyon, 5 katlı çapraz doğrulamayla 3125 eğitim. Budama yok; bu yüzden büyük aramalarda rastgele
  arama ya da daha akıllı yöntemler tercih edilir.

Geri izleme küçük problemlerde kesin cevap verir; büyüdükçe ya iyi bir
budama kuralı gerekir ya da kesin cevaptan vazgeçen yöntemler (açgözlü,
sezgisel).

## Özet

- Geri izleme: seç, devam et, geri al; bütün olasılıkları eksiksiz dener.
- `path.append` / özyineleme / `path.pop`; sonuca `path[:]` (kopya) eklenir.
- Alt kümeler `2ⁿ`, sıralanışlar `n!`: hızla patlar.
- Budama: bir dalın işe yaramayacağı anlaşıldığı an kes; aynı cevap, çok daha
  az düğüm.
- Hazırları `itertools.combinations`, `permutations`, `product`.
