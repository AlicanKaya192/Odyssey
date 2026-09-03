Gerçek kodda böyle satırlar var:

```python
def group(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    ...
```

İlk bakışta okunmuyor. Ama bir yöntemi var ve öğrenilince hepsi aynı.

## Yöntem: en dıştaki kabı bul

Bir belirtim her zaman şu biçimde:

<figure class="fig anat">
  <div class="sig"><u class="m1">dict</u>[<u class="m2">str</u>, <u class="m3">list[int]</u>]</div>
  <ul class="legend">
    <li class="m1"><b>Kap</b> — ilk köşeli parantezden önceki kelime. Bu bir sözlük.</li>
    <li class="m2"><b>Birinci parça</b> — sözlükte bu anahtarların tipi.</li>
    <li class="m3"><b>İkinci parça</b> — değerlerin tipi. Kendisi de bir kap olabilir.</li>
  </ul>
</figure>

Yani üç adım:

1. İlk köşeli parantezden **önceki** kelimeye bak. Kap o.
2. Parantezin içindekileri ayır. `dict` ikiye, `list` bire ayrılır.
3. Ayırdığın parçalardan biri hâlâ kapsa, ona da aynı üç adımı uygula.

## Örnek 1

```python
list[str]
```

- Kap: `list`
- İçinde: `str`

**Metinlerden oluşan liste.** Örnek değer: `["a", "b"]`

## Örnek 2

```python
dict[str, list[int]]
```

- Kap: `dict`, iki parçası var.
- Anahtarlar: `str`
- Değerler: `list[int]` → bu da bir kap, tekrar bakıyoruz: sayı listesi.

**Metin anahtarlı, değerleri sayı listesi olan sözlük.** Örnek değer:

```python
{"Ada": [90, 85], "Alan": [70]}
```

## Örnek 3

```python
list[dict[str, str]]
```

- Kap: `list`
- İçinde: `dict[str, str]` → metin anahtarlı, metin değerli sözlük.

**Sözlüklerden oluşan liste.** Bir tablonun satırları böyle tutuluyor:

```python
[
    {"name": "Ada", "city": "London"},
    {"name": "Alan", "city": "Wilmslow"},
]
```

## Örnek 4 — baştaki satır

Şimdi baştaki zor satıra dönebiliriz:

```python
def group(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
```

**Parametre:** `list[dict[str, str]]` → sözlüklerden oluşan liste. Yani bir
tablonun satırları.

**Dönüş:** `dict[str, list[dict[str, str]]]`

- Kap: `dict`
- Anahtarlar: `str`
- Değerler: `list[dict[str, str]]` → yine satırlardan oluşan bir liste.

**Sonuç:** fonksiyon satırları alıyor, bir metne göre gruplayıp her grubun
satırlarını ayrı liste hâlinde veriyor. Adı zaten `group`; belirtim bunu
doğruluyor.

Fonksiyonun içine hiç bakmadan ne yaptığını anladın. Belirtimin işi tam olarak
bu.

## Sağdan gelen `| None`

Bir belirtimin sonunda `| None` görürsen, o parça en dıştaki tipe aittir:

```python
def find(name: str) -> dict[str, int] | None:
    ...
```

Bu, "sözlük ya da hiçbir şey döndürür" demek — sözlüğün *değerleri*
hakkında bir şey söylemiyor. Karıştırılıyor:

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>SÖZLÜK OLMAYABİLİR</h5>
<pre><code>dict[str, int] | None</code></pre>
    </div>
    <div class="ok">
      <h5>DEĞERLER OLMAYABİLİR</h5>
<pre><code>dict[str, int | None]</code></pre>
    </div>
  </div>
  <figcaption>Soldaki fonksiyon hiç sözlük döndürmeyebilir. Sağdaki her zaman sözlük döndürür ama içindeki bazı değerler boş olabilir. Köşeli parantezin içinde mi dışında mı, tek fark bu.</figcaption>
</figure>

## Takıldığında

Uzun bir belirtim gördüğünde kâğıda yaz ve parantezleri eşleştir. En dıştaki
kabı bulduktan sonra geri kalanı aynı işlemin tekrarı.

Bir de şu işe yarıyor: belirtime uyan **örnek bir değer** yaz. `dict[str,
list[int]]` için `{"a": [1, 2]}` yazdığın an belirtim somutlaşıyor.
