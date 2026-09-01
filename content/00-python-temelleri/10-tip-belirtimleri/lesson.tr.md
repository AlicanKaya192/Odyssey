# Tip Belirtimleri

Başkasının yazdığı bir fonksiyonu açtın ve şunu gördün:

```python
def repeat(text, count):
    return text * count
```

`count` yerine ne vermen gerekiyor? Sayı mı, metin mi? Fonksiyon geriye ne
veriyor? Kodu okumadan bilemiyorsun.

Bu bölüm, Python'a "buraya ne gireceğini ve buradan ne çıkacağını" yazma
biçimini öğretiyor. Adı **tip belirtimi** (type annotation).

## Sorun ne?

Yukarıdaki `repeat` fonksiyonu bir sürü şeyle çalışıyor:

```python
print(repeat("ab", 3))
print(repeat(3, "ab"))
print(repeat([1, 2], 2))
```

```
ababab
ababab
[1, 2, 1, 2]
```

Üçü de çalıştı. Peki yazan kişi hangisini kastetmişti? Belli değil.

Bu, küçük bir dosyada sorun olmuyor. Ama fonksiyon üç ay önce yazıldıysa,
başkası yazdıysa ya da dosya iki bin satırsa, her seferinde kodun içine
girip okumak gerekiyor.

## İlk belirtim

Belirtim, parametrenin yanına iki nokta üst üste ile yazılıyor:

```python
def repeat(text: str, count: int) -> str:
    return text * count
```

Bu satır artık kendi kendini anlatıyor.

<figure class="fig anat">
  <div class="sig">def repeat(<u class="m1">text: str</u>, <u class="m2">count: int</u>) <u class="m3">-&gt; str</u>:</div>
  <ul class="legend">
    <li class="m1"><b>Parametre belirtimi</b> — <code>text</code> bir metin bekliyor.</li>
    <li class="m2"><b>Parametre belirtimi</b> — <code>count</code> bir tam sayı bekliyor.</li>
    <li class="m3"><b>Dönüş belirtimi</b> — fonksiyon geriye metin veriyor. Parantezden sonra <code>-&gt;</code> ile yazılıyor.</li>
  </ul>
</figure>

Okurken şöyle diyorsun: "repeat, bir metin ve bir tam sayı alır, geriye metin
döndürür."

Kullandığın tipler zaten bildiğin tipler:

| Belirtim | Anlamı |
|---|---|
| `str` | Metin |
| `int` | Tam sayı |
| `float` | Ondalıklı sayı |
| `bool` | `True` / `False` |
| `list` | Liste |
| `dict` | Sözlük |
| `None` | Değer yok |

## Python bunu kontrol etmiyor

Buraya dikkat, çünkü en çok yanlış anlaşılan yer burası.

```python
def double(number: int) -> int:
    return number * 2

print(double("ab"))
```

```
abab
```

Hata yok. Program çalıştı. `int` yazmıştık ama metin verdik ve Python
umursamadı.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Sen yazarsın</b><br><code>number: int</code></span>
    <span class="arrow">→</span>
    <span class="node">Python kodu<br>çalıştırır</span>
    <span class="arrow">→</span>
    <span class="node no">Belirtime<br><b>hiç bakmaz</b></span>
  </div>
  <figcaption>Belirtim çalışma anında hiçbir şey yapmaz. Kod, belirtim hiç yazılmamış gibi çalışır.</figcaption>
</figure>

Yani belirtim bir **kural** değil, bir **not**. Peki kime not?

- **Sana.** Üç ay sonra kendi kodunu açtığında.
- **Kodu okuyan başkasına.** Fonksiyonun içine girmeden ne beklediğini görür.
- **Editörüne.** VS Code veya PyCharm belirtimleri okuyor: yanlış tipte bir
  değer verdiğinde daha sen çalıştırmadan altını çiziyor, `text.` yazdığın
  anda da metne ait metotları öneriyor.

Üçüncüsü işin asıl faydası. Belirtim yazmak, hatayı çalışma anından **yazma
anına** çekiyor.

> Belirtim yanlış olsa bile program çalışır. Belirtim koda bir davranış
> **eklemez**, yalnızca niyeti anlatır.

## Değişkenlere belirtim

Değişkenler de belirtim alabiliyor:

```python
count: int = 0
name: str = "Ada"
```

Ama çoğu zaman **gereksiz.** Python `count = 0` satırından zaten tam sayı
olduğunu anlıyor; tekrar yazmak gürültü.

Gerçekten işe yaradığı bir yer var: **boş başlayan kaplar.**

```python
scores = []
```

Bu listenin içinde ne olacak? Sayı mı, metin mi? `[]` boş olduğu için
anlaşılmıyor. Belirtim tam da burada bilgi taşıyor:

```python
scores: list[int] = []
```

## Kabın içinde ne var?

`list` demek "bu bir liste" demek. Ama neyin listesi? Köşeli parantezle
söylüyorsun:

```python
names: list[str] = ["Ada", "Alan"]
ages: dict[str, int] = {"Ada": 36, "Alan": 41}
point: tuple[int, int] = (3, 7)
tags: set[str] = {"python", "basics"}
```

Sözlükte iki tip var, çünkü sözlüğün iki tarafı var:

<figure class="fig anat">
  <div class="sig">ages: <u class="m1">dict</u>[<u class="m2">str</u>, <u class="m3">int</u>]</div>
  <ul class="legend">
    <li class="m1"><b>Kabın kendisi</b> — bu bir sözlük.</li>
    <li class="m2"><b>Anahtarların tipi</b> — <code>"Ada"</code> gibi metinler.</li>
    <li class="m3"><b>Değerlerin tipi</b> — <code>36</code> gibi tam sayılar.</li>
  </ul>
</figure>

İç içe de geçebiliyor. Her öğrencinin not listesini tutan bir sözlük:

```python
grades: dict[str, list[int]] = {
    "Ada": [90, 85],
    "Alan": [70, 95],
}
```

Okurken içten dışa oku: `list[int]` sayı listesi, `dict[str, list[int]]` ise
"metin anahtarlı, sayı listesi değerli sözlük".

## Ya değer yoksa?

Sık karşılaşacağın bir durum: fonksiyon bazen bir şey buluyor, bazen
bulamıyor.

```python
def find_score(name):
    scores = {"Ada": 90}
    if name in scores:
        return scores[name]
    return None
```

Bu fonksiyon bazen `int`, bazen `None` döndürüyor. İkisini de yazabilirsin:

```python
def find_score(name: str) -> int | None:
    scores = {"Ada": 90}
    if name in scores:
        return scores[name]
    return None
```

Dikey çizgi "ya da" demek. `int | None` yani "ya tam sayı ya da hiçbir şey".

Bu belirtim okuyana önemli bir şey söylüyor: **dönen değeri doğrudan kullanma,
önce kontrol et.**

```python
score = find_score("Alan")
if score is None:
    print("not found")
else:
    print(score + 10)
```

Belirtim olmasaydı bu kontrolü yapman gerektiğini ancak program
`TypeError` verdiğinde öğrenirdin.

## Hiçbir şey döndürmeyen fonksiyon

Bazı fonksiyonlar değer döndürmüyor, iş yapıyor:

```python
def greet(name: str) -> None:
    print("hello", name)
```

`-> None` "geriye değer vermiyorum" demek. Bunu yazmak, hiç yazmamaktan
farklı:

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>BELİRTİM YOK</h5>
<pre><code>def greet(name: str):
    print("hello", name)</code></pre>
    </div>
    <div class="ok">
      <h5>BELİRTİLMİŞ</h5>
<pre><code>def greet(name: str) -&gt; None:
    print("hello", name)</code></pre>
    </div>
  </div>
  <figcaption>Soldaki fonksiyon bir değer döndürüyor olabilir de olmayabilir de — okuyan bilemiyor. Sağdaki açıkça "döndürmüyorum" diyor.</figcaption>
</figure>

`print` ile `return` yeni başlayanlarda sık karışıyor; `-> None` bu farkı
görünür yapıyor.

## Eski kodda göreceğin biçim

Bir kütüphaneye baktığında şöyle satırlarla karşılaşacaksın:

```python
from typing import List, Dict, Optional

def load(path: str) -> Optional[List[Dict[str, int]]]:
    ...
```

Bunlar aynı şeyin eski yazımı. Python 3.9 öncesinde `list[str]` yazılamıyordu;
`typing` modülünden `List[str]` almak gerekiyordu.

| Eski | Yeni |
|---|---|
| `List[str]` | `list[str]` |
| `Dict[str, int]` | `dict[str, int]` |
| `Tuple[int, int]` | `tuple[int, int]` |
| `Optional[str]` | `str \| None` |
| `Union[int, str]` | `int \| str` |

Yeni kod yazarken sağdaki sütunu kullan. Soldakini tanıman yeterli — çünkü
karşına çıkacak.

## Nereye yazılır, nereye gerekmez

Belirtim her satıra yazılacak bir şey değil. Faydası en yüksek yerler:

- **Fonksiyon imzaları.** Buraya yaz. Bir fonksiyonu kullanan kişinin gördüğü
  tek şey imzadır.
- **Boş başlayan kaplar.** `results: list[str] = []`
- **Anlamı belirsiz değerler.** `timeout: float = 0.5`

Gereksiz olduğu yerler:

- **Değeri apaçık atamalar.** `name = "Ada"` satırına `: str` eklemek bilgi
  katmıyor.
- **Döngü değişkenleri.** `for item in items:` içinde belirtime gerek yok.
- **Kısa ve tek kullanımlık ara değerler.**

Ölçüt basit: **belirtim bir soruyu cevaplıyorsa yaz, kendini tekrar ediyorsa
yazma.**

## Özet

- Tip belirtimi, bir değerin hangi tipte olması beklendiğini yazma biçimidir:
  `text: str`, `-> int`.
- Parametreye iki nokta ile, dönüşe parantezden sonra `->` ile yazılır.
- **Python bunları çalışma anında kontrol etmez.** Yanlış tip verirsen hata
  almazsın; belirtim bir kural değil, bir nottur.
- Faydası okuyan insana ve editöre: hatalar kod çalıştırılmadan görünür olur.
- Kabın içindeki tip köşeli parantezle yazılır: `list[str]`, `dict[str, int]`,
  `dict[str, list[int]]`.
- Değer olmayabiliyorsa `int | None` yazılır; okuyan kişi kontrol etmesi
  gerektiğini anlar.
- Değer döndürmeyen fonksiyon `-> None` alır.
- Eski kodda `List[str]` ve `Optional[str]` görürsün; yenisi `list[str]` ve
  `str | None`.
- Her yere değil, soru cevaplayan yerlere yazılır — en başta fonksiyon
  imzalarına.
