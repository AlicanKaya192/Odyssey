Köşeli parantez yerine normal parantez yazdığında ortaya liste değil bir
**üreteç** çıkıyor. Fark tek cümlede: liste bütün elemanları belleğe
kuruyor, üreteç elemanları istendikçe tek tek veriyor.

```python
numbers = [1, 2, 3, 4, 5]

liste = [n * n for n in numbers]
uretec = (n * n for n in numbers)

print(liste)
print(uretec)
```

```
[1, 4, 9, 16, 25]
<generator object <genexpr> at 0x000001>
```

Üreteç henüz hiçbir şey hesaplamadı; yalnızca "istenirse şunu üretirim"
diyor.

## Nerede işe yarar

```python
total = sum(n * n for n in numbers)
```

Toplamı alırken bütün kareleri saklamaya gerek yok: her kare üretiliyor,
toplama ekleniyor ve unutuluyor. Bir milyon satırlık dosyada bu, belleği
doldurmakla doldurmamak arasındaki fark.

Aynı şey `any` ve `all` ile daha da belirgin:

```python
has_negative = any(n < 0 for n in numbers)
```

`any`, ilk `True` değerini görünce **durur**; listenin geri kalanı hiç
hesaplanmaz.

## Tek kullanımlık

Üreteç bir kez dolaşılıyor:

```python
uretec = (n * n for n in numbers)

print(sum(uretec))
print(sum(uretec))
```

```
55
0
```

İkinci toplam sıfır, çünkü üreteç tükendi. Aynı veriyi iki kez
kullanacaksan liste kur.

## Hangisini seçmeli

<figure class="fig versus">
  <div class="ok">
    <h4>Liste</h4>
    <p>Sonucu birden fazla kez kullanacaksan, uzunluğunu soracaksan
    (<code>len</code>), sıra numarasıyla erişeceksen.</p>
  </div>
  <div class="dim">
    <h4>Üreteç</h4>
    <p>Sonucu bir kez dolaşacaksan ve veri büyükse; <code>sum</code>,
    <code>any</code>, <code>all</code>, <code>max</code> gibi bir işlemin
    içine doğrudan veriyorsan.</p>
  </div>
</figure>

## Tek parantez yeter

Üreteç bir fonksiyonun tek argümanıysa ayrıca parantez açmaya gerek yok:

```python
total = sum(n * n for n in numbers)        # doğru
total = sum((n * n for n in numbers))      # gereksiz parantez
```

İki argüman varsa parantez gerekiyor:

```python
print(max((n for n in numbers), default=0))
```
