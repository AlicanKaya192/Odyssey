# Metinleri Biçimlendirme

Ekrana yazdırdığın her şey bir metin. Sayıyı olduğu gibi yazdırmak çoğu
zaman yetmiyor: para üç basamak uzuyor, tablonun sütunları kayıyor, yüzde
elle hesaplanıyor.

f-string'in içinde iki nokta üst üsteden sonra yazılan kısım bu işi
yapıyor. Adı **biçim belirteci**.

## Önce sorun

```python
price = 12.5
total = 1234567.891
rate = 0.0725

print(f"Fiyat: {price}")
print(f"Toplam: {total}")
print(f"Oran: {rate}")
```

```
Fiyat: 12.5
Toplam: 1234567.891
Oran: 0.0725
```

Fiyatın kuruşu eksik, toplam okunmuyor, oranın yüzde kaç olduğu belli
değil. Üçü de tek bir yazımla düzeliyor.

## İki nokta üst üste

<figure class="fig anat">
  <div class="sig">f"{<u class="m1">total</u><u class="m2">:</u><u class="m3">,.2f</u>}"</div>
  <ul class="legend">
    <li class="m1"><b>Değer</b> — yazdırılacak şey. Değişken ya da ifade.</li>
    <li class="m2"><b>İki nokta üst üste</b> — buradan sonrası biçim.</li>
    <li class="m3"><b>Biçim belirteci</b> — nasıl görüneceği: ayırıcı, basamak, tür.</li>
  </ul>
</figure>

Belirteç değeri **değiştirmiyor**, yalnızca ekrandaki hâlini belirliyor.
`total` hâlâ `1234567.891`.

## Ondalık basamak: `.2f`

```python
price = 12.5
print(f"Fiyat: {price:.2f}")
print(f"Pi: {3.14159:.3f}")
```

```
Fiyat: 12.50
Pi: 3.142
```

Noktadan sonraki sayı kaç basamak istediğini, `f` ise ondalık sayı
istediğini söylüyor. Eksik basamak sıfırla tamamlanıyor, fazlası
yuvarlanıyor.

## Binlik ayırıcı: `,`

```python
total = 1234567.891
print(f"Toplam: {total:,}")
print(f"Toplam: {total:,.2f}")
```

```
Toplam: 1,234,567.891
Toplam: 1,234,567.89
```

Virgül üç basamakta bir ayırıcı koyuyor. Sırası önemli: **önce ayırıcı,
sonra basamak** (`,.2f`).

## Yüzde: `%`

```python
rate = 0.0725
print(f"Oran: {rate:.1%}")
```

```
Oran: 7.2%
```

`%` iki şeyi birden yapıyor: yüzle çarpıyor ve sonuna işareti koyuyor.
Elde `0.0725` varken `{rate * 100:.1f}%` yazmak da aynı sonucu veriyor,
ama `%` daha kısa ve çarpmayı unutma ihtimalin yok.

## Genişlik ve hizalama

Sayının önüne yazılan sayı **en az kaç karakter** yer kaplayacağını
söylüyor:

```python
print(f"[{42:6}]")
print(f"[{'ada':6}]")
```

```
[    42]
[ada   ]
```

Sayı sağa, metin sola yaslanıyor. Bunu kendin de seçebilirsin:

<figure class="fig anat">
  <div class="anat-row"><span><code>:&lt;10</code></span><span>Sola yasla, on karaktere tamamla</span></div>
  <div class="anat-row"><span><code>:&gt;10</code></span><span>Sağa yasla</span></div>
  <div class="anat-row"><span><code>:^10</code></span><span>Ortala</span></div>
  <div class="anat-row"><span><code>:*^10</code></span><span>Ortala, boşluk yerine yıldızla doldur</span></div>
</figure>

## Tabloyu hizalamak

Hizalamanın asıl işe yaradığı yer bu:

```python
products = [("Kalem", 3, 12.5), ("Defter", 12, 145.0), ("Silgi", 5, 7.25)]

for name, count, price in products:
    print(f"{name:<10}{count:>4}{price:>10.2f}")
```

```
Kalem        3     12.50
Defter      12    145.00
Silgi        5      7.25
```

Ad sola yaslı on karakter, adet sağa yaslı dört, fiyat sağa yaslı on ve
iki basamak. Sütunlar alt alta duruyor, çünkü her alanın genişliği sabit.

## Sıfırla doldurmak

```python
for day in [1, 9, 15]:
    print(f"2026-09-{day:02d}")
```

```
2026-09-01
2026-09-09
2026-09-15
```

`d` tam sayı demek, `02` ise "en az iki karakter, eksiği sıfırla tamamla".
Saat, tarih ve sipariş numarası yazarken sık gerekiyor.

## Artı işaretini göstermek

```python
change = 4.2
print(f"Değişim: {change:+.1f}")
print(f"Değişim: {-change:+.1f}")
```

```
Değişim: +4.2
Değişim: -4.2
```

Artı işareti varsayılan olarak yazılmıyor; `+` onu da yazdırıyor. Artan
ve azalan değerleri yan yana gösterirken işe yarıyor.

## Hata ayıklarken: `=`

```python
count = 7
print(f"{count = }")
```

```
count = 7
```

Değişkenin adını da değerini de yazıyor. Kodu incelerken
`print("count:", count)` yazmaktan kısa.

## `round()` ile aynı şey değil

```python
price = 12.5
rounded = round(price, 2)

print(rounded)
print(f"{price:.2f}")
```

```
12.5
12.50
```

`round()` **sayıyı** değiştiriyor ve sondaki sıfırı taşımıyor; biçim
belirteci **görünüşü** değiştiriyor. Ekrana yazdırırken biçim belirteci,
hesaba devam edecekse `round()` kullanılıyor.

## Özet

- Biçim iki nokta üst üsteden sonra yazılıyor: `f"{deger:belirteç}"`.
- `.2f` ondalık basamak, `,` binlik ayırıcı, `%` yüzde.
- Sıralama: `[doldurma][hizalama][işaret][genişlik][,][.basamak][tür]`.
- `<` sola, `>` sağa, `^` ortaya yaslıyor; genişlik sütunları hizalıyor.
- `02d` sıfırla dolduruyor, `+` artı işaretini gösteriyor.
- Belirteç sayıyı değiştirmiyor, yalnızca ekrandaki hâlini.
