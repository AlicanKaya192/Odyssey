# İki İşaretçi ve Kayan Pencere

Bir listede "şu şartı sağlayan ikili" ya da "şu şartı sağlayan ardışık
parça" aranırken ilk akla gelen çözüm her ikiliyi, her parçayı denemek:
`O(n²)`. Bu bölümdeki iki teknik aynı soruları **listeyi bir kez gezerek**
çözüyor: **iki işaretçi (two pointers)** ve **kayan pencere (sliding
window)**. İkisinde de fikir aynı: önceki adımda öğrendiğini atmamak.

## İki işaretçi: iki uçtan içeri

**Problem:** sıralı bir fiyat listesinde toplamı tam `target` olan iki fiyat
var mı?

Kaba kuvvet her ikiliyi dener. İki işaretçi ise bir işaretçiyi başa (`left`),
birini sona (`right`) koyar ve toplama bakar:

- Toplam **küçükse**: daha büyük bir sayı gerek; `left` bir sağa.
- Toplam **büyükse**: daha küçük bir sayı gerek; `right` bir sola.
- **Eşitse**: bulduk.

```python
def pair_two_pointers(items, target):
    left, right = 0, len(items) - 1
    while left < right:
        total = items[left] + items[right]
        if total == target:
            return items[left], items[right]
        if total < target:
            left += 1          # daha büyük bir sayı lazım
        else:
            right -= 1         # daha küçük bir sayı lazım
    return None
```

**Neden doğru?** Toplam küçükken `left`'i atlamak güvenli: `items[left]` en
büyük sayıyla (`items[right]`) bile hedefe ulaşamıyor, demek ki hiçbir ikilide
işe yaramaz. Büyükken `right` için aynı mantık. Her adımda bir aday kesin
olarak eleniyor ve işaretçiler en fazla `n` adımda buluşuyor: `O(n)`.

İki fonksiyona da bir adım sayacı ekleyip kaba kuvvetle karşılaştırdık
(10 000 sıralı fiyat):

```text
((0, 19990), 9995)
((0, 19990), 5)
(None, 49995000)
(None, 9999)
```

Sütunlar: bulunan ikili ve adım sayısı. İlk iki satır cevabın listenin iki
ucunda olduğu durum; son iki satır **cevap yokken**: kaba kuvvet her ikiliyi
(neredeyse 50 milyon) denemek zorunda, iki işaretçi 9 999 adımda "yok"
diyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>[1, 3, 4, 6, 9]</code>, hedef 10</span><span>left → 1, right → 9: toplam 10, bulundu</span></div>
    <div class="anat-row"><span><code>[1, 3, 4, 6, 9]</code>, hedef 7</span><span>1 + 9 = 10 büyük → right sola (6)</span></div>
    <div class="anat-row"><span></span><span>1 + 6 = 7, bulundu</span></div>
    <div class="anat-row"><span><code>[1, 3, 4, 6, 9]</code>, hedef 14</span><span>1 + 9 = 10 küçük → left sağa; 3 + 9 = 12 küçük → left sağa; 4 + 9 = 13 küçük → left sağa; 6 + 9 = 15 büyük → right sola; işaretçiler buluştu: yok</span></div>
  </div>
  <figcaption>Her adımda bir aday kesin olarak eleniyor; işaretçiler hiç geri gitmiyor.</figcaption>
</figure>

Ön koşul: liste **sıralı**. Sırasız listede aynı soru için bir önceki
bölümlerdeki kümeyle bakma yöntemi kullanılır (Hash bölümünde ayrıntısı).

## Aynı yönde iki işaretçi: hızlı ve yavaş

İşaretçiler aynı yönde de yürüyebilir. Sıralı bir listedeki tekrarları
**yerinde** atmak:

```python
def remove_duplicates(items):
    if not items:
        return 0
    slow = 0                              # son yazılan benzersiz değerin yeri
    for fast in range(1, len(items)):     # okuyan işaretçi
        if items[fast] != items[slow]:
            slow += 1
            items[slow] = items[fast]
    return slow + 1                       # benzersiz eleman sayısı
```

`fast` her elemanı okuyor, `slow` yalnızca yeni bir değer görünce yazıyor.
Ek liste yok: `O(n)` süre, `O(1)` ek bellek.

## Kayan pencere: sabit boy

**Problem:** günlük satışlarda, art arda gelen `k` günün toplamı en fazla
hangi dönemde?

Kaba kuvvet her başlangıç günü için `k` sayıyı baştan toplar: `O(n × k)`.
Ama bir pencereyi bir gün kaydırınca toplamın değişen yalnızca iki parçası
var: **giren gün eklenir, çıkan gün çıkarılır**.

```python
def best_window(values, k):
    total = sum(values[:k])               # ilk pencere
    best = total
    for i in range(k, len(values)):
        total += values[i] - values[i - k]   # giren - çıkan
        if total > best:
            best = total
    return best
```

10 000 günde 500 günlük pencere için iki yöntemin attığı adımları (her
toplamayı sayarak) ölçtük:

```text
(26476, 4750500)
(26476, 10000)
```

Aynı cevap (ilk sayı), yaklaşık 475 kat daha az iş.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Değerler</span><span><code>[4, 2, 7, 1, 8, 3]</code>, k = 3</span></div>
    <div class="anat-row"><span>Pencere 1: 4, 2, 7</span><span>toplam 13</span></div>
    <div class="anat-row"><span>Pencere 2: 2, 7, 1</span><span>13 + 1 − 4 = 10</span></div>
    <div class="anat-row"><span>Pencere 3: 7, 1, 8</span><span>10 + 8 − 2 = 16</span></div>
    <div class="anat-row"><span>Pencere 4: 1, 8, 3</span><span>16 + 3 − 7 = 12</span></div>
  </div>
  <figcaption>Her kaydırmada yalnızca iki işlem: giren eklenir, çıkan çıkarılır. En büyük toplam 16.</figcaption>
</figure>

## Kayan pencere: değişken boy

Bazen pencerenin boyu sabit değildir; bir **şart** sağlandığı sürece büyür,
bozulunca soldan küçülür. Örnek: bir metinde **harf tekrarı olmayan en uzun
parça**.

```python
def longest_unique(text):
    last_seen = {}                 # harf → en son görüldüğü indeks
    start = 0                      # pencerenin sol ucu
    best = 0
    for end, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1     # tekrar: sol ucu tekrarın arkasına al
        last_seen[ch] = end
        best = max(best, end - start + 1)
    return best

for t in ["abcabcbb", "bbbbb", "pwwkew", ""]:
    print(repr(t), longest_unique(t))
```

```text
'abcabcbb' 3
'bbbbb' 1
'pwwkew' 3
'' 0
```

Sağ uç (`end`) her adımda bir ilerliyor, sol uç (`start`) yalnızca ileri
gidiyor; ikisi toplamda en fazla `n` adım atıyor: `O(n)`. Her olası parçayı
denemek `O(n²)` (hatta parçanın tekrarsız olduğunu denetlemekle `O(n³)`)
olurdu.

## Hangi problemde hangisi?

- **Sıralı listede ikili/üçlü arama** (toplamı şu olan, farkı şu olan):
  iki uçtan işaretçi.
- **Yerinde düzenleme** (tekrarları at, sıfırları sona taşı): hızlı ve yavaş
  işaretçi.
- **Ardışık parça** (en büyük toplam, ortalama, şartı sağlayan en kısa/en
  uzun parça): kayan pencere.

Ortak ipucu: problem "ardışık" ya da "sıralı" diyorsa ve kaba kuvvet iç içe
döngüyse, işaretçilerin yalnızca **ileri** gittiği bir çözüm büyük ihtimalle
var.

## Özet

- İki işaretçi: sıralı listede iki uçtan içeri; her adım bir adayı eler,
  `O(n)`.
- Hızlı/yavaş işaretçi: aynı yönde, yerinde düzenleme, `O(1)` ek bellek.
- Sabit pencere: kaydırırken giren eklenir, çıkan çıkarılır; `O(n × k)`
  yerine `O(n)`.
- Değişken pencere: şart bozulunca sol uç ilerler; iki uç toplam `O(n)` adım.
- İşaretçiler geri gitmediği sürece toplam iş doğrusal kalır.
