# Algoritma Nedir?

Bir yemek tarifi düşün: malzemeler belli, adımlar sıralı, her adım açık
("suyu kaynat", "makarnayı ekle, 8 dakika bekle") ve sonunda bir yemek
çıkıyor. **Algoritma** da budur: bir problemi çözmek için **sırası belli,
açık ve sonunda biten adımlar**.

Bilgisayar tarifi kendisi uyduramaz; ona adımları sen verirsin. Bu
patikada kodu çalıştırmaktan bir adım öteye geçeceğiz: bir problemi
**adımlara bölmeyi**, o adımların **doğru** olduğundan emin olmayı ve iki
farklı çözümden **hangisinin daha iyi** olduğunu söylemeyi öğreneceğiz.

## Girdi, adımlar, çıktı

Her algoritmanın üç parçası var:

- **Girdi (input):** algoritmanın üzerinde çalıştığı veri. Örneğin bir
  sayı listesi.
- **Adımlar:** girdiyi işleyen talimatlar.
- **Çıktı (output):** sonuç. Örneğin listedeki en büyük sayı.

<figure class="fig">
  <div class="flow">
    <span class="node">Girdi: [3, 8, 2, 9, 4]</span><span class="arrow">→</span>
    <span class="node">Adımlar</span><span class="arrow">→</span>
    <span class="node acc">Çıktı: 9</span>
  </div>
  <figcaption>Algoritma girdiyi çıktıya çeviren adımlar dizisi. Aynı girdi her seferinde aynı çıktıyı vermeli.</figcaption>
</figure>

## İlk algoritma: en büyük sayıyı bulmak

Önüne bir deste kâğıt konduğunu, her kâğıtta bir sayı yazdığını düşün.
En büyüğünü nasıl bulursun? Muhtemelen şöyle:

1. İlk kâğıda bak, sayıyı aklında tut: "şimdilik en büyük bu".
2. Sıradaki kâğıda bak. Aklındakinden büyükse aklındakini bununla değiştir.
3. Kâğıt kalmayana kadar 2. adımı tekrarla.
4. Aklında kalan sayı en büyüğüdür.

Bu dört satır bir algoritma. Henüz Python değil, ama her adım açık. Böyle
**programlama dilinden bağımsız**, adımları insan diline yakın yazmaya
**sözde kod (pseudocode)** denir:

```text
en_buyuk ← listenin ilk elemanı
listedeki her sayı için:
    eğer sayı > en_buyuk ise:
        en_buyuk ← sayı
sonuç: en_buyuk
```

`←` "şunu şuna ata" demek. Sözde kodun kuralları gevşektir; amaç, kodu
yazmadan önce fikri netleştirmek. Python'a çevirmek artık neredeyse
kelimesi kelimesine:

```python
def find_largest(numbers):
    largest = numbers[0]
    for number in numbers:
        if number > largest:
            largest = number
    return largest

print(find_largest([3, 8, 2, 9, 4]))
```

```text
9
```

"Python'da zaten `max()` var" diyebilirsin, haklısın. Ama `max()`'ın
içinde de tam olarak bu döngü dönüyor. Hazır fonksiyonun içini bilmeyen,
hazırı olmayan bir problemle karşılaşınca ne yapacağını bilemez. Bu
patikada hazır fonksiyonları bilerek bir kenara bırakıp algoritmaları
kendimiz yazacağız; sonra hangi hazır aracın ne zaman işe yaradığını
çok daha iyi anlayacağız.

## İyi bir algoritmanın özellikleri

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Girdi ve çıktı</span><span>Neyle çalıştığı ve ne ürettiği belli.</span></div>
    <div class="anat-row"><span>Belirlilik</span><span>Her adım tek anlamlı; iki kişi aynı adımı aynı şekilde uygular.</span></div>
    <div class="anat-row"><span>Sonluluk</span><span>Her girdide bir noktada biter; sonsuza kadar dönmez.</span></div>
    <div class="anat-row"><span>Doğruluk</span><span>Yalnızca örnekte değil, geçerli her girdide doğru sonucu verir.</span></div>
    <div class="anat-row"><span>Verimlilik</span><span>Gereğinden fazla adım atmaz; girdi büyüyünce makul kalır.</span></div>
  </div>
  <figcaption>Bir tarif de bu beş özelliği taşır: malzemeler, net adımlar, biten bir süreç, doğru yemek ve makul bir süre.</figcaption>
</figure>

Bunlardan en çok atlananı **doğruluk**: algoritma, örnekte doğru sonuç
verdi diye her girdide doğru çalışmaz.

## Uç durumlar: algoritmanın gerçek sınavı

Aynı problemi biraz farklı çözen birini düşün: "en büyüğü sıfırdan başlatırım,
nasılsa her sayı sıfırdan büyüktür".

```python
def find_largest_wrong(numbers):
    largest = 0
    for number in numbers:
        if number > largest:
            largest = number
    return largest

print(find_largest_wrong([3, 8, 2, 9, 4]))
print(find_largest_wrong([-5, -2, -9]))
```

```text
9
0
```

İlk liste doğru, ikincisi **yanlış**: listede olmayan `0`'ı döndürdü. "Her
sayı sıfırdan büyüktür" varsayımı negatif sayılarda çöktü. İlk elemandan
başlatan sürüm bu tuzağa düşmüyor:

```python
print(find_largest([-5, -2, -9]))
```

```text
-2
```

Algoritmanın sıradan girdilerde değil, **kenarda kalan girdilerde** bozulma
ihtimali en yüksektir. Bunlara **uç durum (edge case)** denir. Bir
algoritmayı yazınca kendine şu soruları sor:

- **Boş girdi:** liste boşsa ne olur? (`find_largest([])` hata verir:
  `numbers[0]` yok. Ya bunu belgeleriz ya da özel bir değer döndürürüz.)
- **Tek eleman:** tek sayılık listede doğru mu?
- **Hepsi aynı:** `[7, 7, 7]`?
- **Negatifler ve sıfır:** az önceki hata tam burada çıktı.
- **Sıra:** cevap baştaysa, sondaysa, ortadaysa?

Alıştırmalardaki denetimler de kodunu tam bu girdilerle deneyecek.

## Aynı problem, iki algoritma

Bir problemin çoğu zaman birden fazla doğru algoritması vardır. 1'den
`n`'e kadar sayıların toplamını düşünelim. İlk akla gelen yol tek tek
toplamak:

```python
def sum_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
```

Bir de rivayete göre Gauss'un çocukken bulduğu yol var: 1 ile 100'ü, 2 ile
99'u eşleştirirsen her çift 101 eder ve 50 çift vardır. Genel hâli
`n × (n + 1) / 2`:

```python
def sum_formula(n):
    return n * (n + 1) // 2

print(sum_loop(100), sum_formula(100))
print(sum_loop(1_000_000) == sum_formula(1_000_000))
```

```text
5050 5050
True
```

İkisi de doğru. Peki hangisi daha iyi?

<figure class="fig">
  <div class="versus">
    <div><h4>Döngüyle toplamak</h4>
      <p><code>n</code> sayıyı tek tek ekler.</p>
      <p><code>n = 100</code> → 100 toplama<br><code>n = 1 000 000</code> → 1 000 000 toplama</p>
      <p>Adım sayısı <b><code>n</code> ile birlikte büyüyor</b>.</p></div>
    <div class="ok"><h4>Formülle</h4>
      <p>Bir çarpma, bir toplama, bir bölme.</p>
      <p><code>n = 100</code> → 3 işlem<br><code>n = 1 000 000</code> → 3 işlem</p>
      <p>Adım sayısı <b>sabit</b>.</p></div>
  </div>
  <figcaption>İkisi de doğru sonucu veriyor; fark, girdi büyüdükçe yapılan işin nasıl büyüdüğünde.</figcaption>
</figure>

`n` 100 iken fark önemsiz. `n` bir milyar olunca döngü bir milyar
toplama yapar, formül yine birkaç işlem. **Algoritmayı karşılaştırırken
saniyeye değil, girdi büyüdükçe adım sayısının nasıl büyüdüğüne
bakarız.** Bir sonraki bölümün konusu tam olarak bu: karmaşıklık ve
Büyük O gösterimi.

## Algoritmayı izlemek

Bir algoritmayı anlamanın en iyi yolu onu adım adım izlemek: hangi satır
çalıştı, değişkenler nasıl değişti? Bu patikadaki alıştırmalarda kodunu
yazdıktan sonra **Çalıştır**'ın yanındaki **Adım adım** düğmesine bas;
`largest`'ın döngü boyunca nasıl değiştiğini satır satır göreceksin.
Takıldığında aynı düğmeyle örnek çözümü de izleyebilirsin.

## Özet

- Algoritma; girdiyi çıktıya çeviren, sırası belli, açık ve biten adımlar.
- Önce fikri **sözde kodla** yaz, sonra Python'a çevir.
- Doğruluk, örnekte çalışmak değil **her girdide** çalışmaktır; uç durumları
  (boş, tek eleman, negatif, hepsi aynı) mutlaka dene.
- Aynı problemin birden fazla algoritması olabilir; karşılaştırırken girdi
  büyüdükçe **adım sayısının** nasıl arttığına bakılır.
