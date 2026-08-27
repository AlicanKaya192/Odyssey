Dilimleme (slicing) listelerin en kullanışlı özelliklerinden biri. Kuralı bir
kez oturttuğunda metinlerde de aynı şekilde çalıştığını göreceksin.

## Temel biçim

```python
liste[baslangic:bitis]
```

**Başlangıç dâhil, bitiş hariç.** Bu tek cümle dilimlemenin yarısıdır.

```python
numbers = [0, 1, 2, 3, 4, 5]

print(numbers[2:5])     # [2, 3, 4]     5 yok
```

Bu kural garip görünebilir ama bir faydası var: `bitis - baslangic` sana kaç
eleman aldığını doğrudan veriyor. `numbers[2:5]` üç eleman.

## Uçları boş bırakmak

```python
print(numbers[:3])      # [0, 1, 2]              bastan
print(numbers[3:])      # [3, 4, 5]              sona kadar
print(numbers[:])       # [0, 1, 2, 3, 4, 5]     hepsi
```

`liste[:]` listenin **kopyasını** verir. Bu önemli, birazdan değineceğiz.

## Negatif sayılarla

```python
print(numbers[-3:])     # [3, 4, 5]     son uc eleman
print(numbers[:-1])     # [0, 1, 2, 3, 4]   sonuncu haric
```

`liste[-3:]` kalıbını çok kullanacaksın: "son üç tanesini ver".

## Adım

Üçüncü bir sayı adım aralığını belirler:

```python
print(numbers[::2])     # [0, 2, 4]     birer atlayarak
print(numbers[1::2])    # [1, 3, 5]     1'den baslayip atlayarak
print(numbers[::-1])    # [5, 4, 3, 2, 1, 0]   ters cevirir
```

`[::-1]` listeyi ters çevirmenin en kısa yolu.

## Aralık dışına taşmak hata değil

Sıra numarası isterken sınırı aşarsan hata alırsın, ama dilim alırken almazsın:

```python
print(numbers[10])      # IndexError
print(numbers[2:100])   # [2, 3, 4, 5]   sorun yok
print(numbers[100:])    # []             bos liste
```

Dilimleme sessizce elindekini verir. Bu bazen işine yarar, bazen de hatayı
gizler — listenin boş dönmesi beklediğin bir şey değilse kontrol etmen gerekir.

## Kopya meselesi

Bir listeyi başka bir değişkene atamak **kopya oluşturmaz**; ikisi aynı listeyi
gösterir:

```python
a = [1, 2, 3]
b = a
b.append(4)

print(a)     # [1, 2, 3, 4]   a da degisti
```

Gerçekten ayrı bir kopya istiyorsan dilim al:

```python
a = [1, 2, 3]
b = a[:]
b.append(4)

print(a)     # [1, 2, 3]      a olduğu gibi
print(b)     # [1, 2, 3, 4]
```

Bu, yeni başlayanların en çok şaşırdığı davranışlardan biri. Aklında tutmaya
değer.
