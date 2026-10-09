# Yığın ve Kuyruk

Bazı algoritmalarda verinin **hangi sırayla** işleneceği her şeydir. İki
temel yapı bu sırayı belirler:

- **Yığın (stack):** son giren ilk çıkar (LIFO, *last in, first out*). Üst üste
  konmuş tabaklar: en son koyduğunu ilk alırsın.
- **Kuyruk (queue):** ilk giren ilk çıkar (FIFO, *first in, first out*). Gişe
  sırası: önce gelen önce hizmet alır.

İkisi de yalnızca **iki işlemi** sabit sürede yapar: bir uçtan eklemek, bir
uçtan almak. Bu kısıtlama bir zayıflık değil, güç: algoritma "sıradaki kim?"
sorusunu hiç düşünmek zorunda kalmaz.

## Python'da yığın: liste

Listenin **sonu** yığının üstüdür: `append` ile koy, `pop` ile al. İkisi de
`O(1)`. Üstteki elemana almadan bakmak için `stack[-1]`.

```python
history = []
history.append("yaz: merhaba")
history.append("yaz: dunya")
history.append("sil: dunya")
print(history.pop())       # en son yapılan geri alınır
print(history[-1])         # sıradaki geri alınacak
```

Metin düzenleyicideki **geri al (Ctrl+Z)** tam olarak bir yığın: en son
yaptığın, ilk geri alınır. Bir önceki bölümlerdeki **çağrı yığını** da öyle:
en son çağrılan fonksiyon ilk biter.

## Yığın uygulaması 1: parantez denetimi

Bir ifadedeki parantezler düzgün kapanıyor mu? `(a[b]{c})` doğru, `(a[b)]`
yanlış. Açılan her parantezi yığına koy; kapanan bir parantez görünce
yığının **üstündeki** onun eşi mi diye bak. Neden üstteki? Çünkü en son açılan
parantez ilk kapanmalı: tam olarak LIFO.

```python
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack           # açılıp kapanmayan kaldıysa False

for t in ["(a[b]{c})", "(a[b)]", "((", ""]:
    print(repr(t), is_balanced(t))
```

```text
'(a[b]{c})' True
'(a[b)]' False
'((' False
'' True
```

Üç tuzak, üçü de kodda: kapanan parantez geldiğinde yığın **boş** olabilir
(`")("`); üstteki parantez **yanlış türde** olabilir (`(a[b)]`); ve sonunda
yığında **açık kalan** parantez olabilir (`((`).

## Yığın uygulaması 2: postfix hesaplama

`(3 + 4) * 2` ifadesini bilgisayara parantezsiz anlatmanın bir yolu
**postfix** (ters Lehçe gösterimi): işlemciler sayılardan **sonra** gelir:
`3 4 + 2 *`. Hesaplamak için tek yığın yeter: sayıyı yığına koy; işlemci
görünce üstteki iki sayıyı al, işlemi yap, sonucu geri koy.

```python
def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if token in "+-*/":
            right = stack.pop()        # sıra önemli: önce sağdaki çıkar
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(left / right)
        else:
            stack.append(float(token))
        print(token, stack)
    return stack.pop()

print(eval_postfix(["3", "4", "+", "2", "*"]))
```

```text
3 [3.0]
4 [3.0, 4.0]
+ [7.0]
2 [7.0, 2.0]
* [14.0]
14.0
```

Hesap makineleri ve derleyiciler ifadeleri içeride buna benzer biçimde
hesaplar.

## Yığın uygulaması 3: sıradaki büyük eleman

Günlük sıcaklıklarda her gün için "kendinden **sonraki ilk daha sıcak** gün
kaç derece?" sorusu. Kaba kuvvet her gün için ileriye bakar: `O(n²)`. **Monoton
yığın** ise henüz cevabını bulamamış günleri yığında bekletir; yığındaki
değerler hep azalan sırada durur. Yeni bir gün geldiğinde, yığının üstündeki
kendinden soğuk günlerin hepsinin cevabı odur:

```python
def next_greater(values):
    result = [-1] * len(values)
    stack = []                                # cevap bekleyen günlerin indeksleri
    for i, x in enumerate(values):
        while stack and values[stack[-1]] < x:
            result[stack.pop()] = x           # bekleyenin cevabı bulundu
        stack.append(i)
    return result
```

`[2, 7, 3, 5, 4, 6, 8]` için ve azalan 5000 sıcaklık için iki yöntemi adım
sayarak karşılaştırdık:

```text
([7, 8, 5, 6, 6, 8, -1], 13)
True 12497500 5000
```

İlk satır sonuç ve monoton yığının adımları. İkinci satırda (azalan sıralı,
kaba kuvvetin en kötü günü) sonuçlar aynı, ama kaba kuvvet 12,5 milyon adım,
monoton yığın 5000 adım attı. İçteki `while`'a rağmen `O(n)`: her gün yığına
**bir kez** girip **en fazla bir kez** çıkıyor.

## Python'da kuyruk: deque

Listeden baştan `pop(0)` almak bütün listeyi kaydırır (`O(n)`); bunu iki
bölüm önce ölçmüştük. Kuyruk için `collections.deque`: `append` ile sona
ekle, `popleft` ile baştan al, ikisi de `O(1)`.

```python
from collections import deque

queue = deque()
queue.append("Ada")
queue.append("Bora")
queue.append("Cem")
print(queue.popleft())     # ilk gelen
print(list(queue))
```

<figure class="fig">
  <div class="versus">
    <div><h4>Yığın (LIFO)</h4>
      <p>Ekle: <code>append</code> → sona<br>Al: <code>pop()</code> ← sondan</p>
      <p>1, 2, 3 eklenince alış sırası: <b>3, 2, 1</b></p>
      <p>Geri alma, parantezler, derine dalma</p></div>
    <div class="ok"><h4>Kuyruk (FIFO)</h4>
      <p>Ekle: <code>append</code> → sona<br>Al: <code>popleft()</code> ← baştan</p>
      <p>1, 2, 3 eklenince alış sırası: <b>1, 2, 3</b></p>
      <p>Sırayla işlem, katman katman gezme</p></div>
  </div>
  <figcaption>İkisi de sona ekler; fark, hangi uçtan alındığında.</figcaption>
</figure>

## Kuyruk nerede kullanılır?

- **Sırayla işlenen işler:** yazıcı kuyruğu, istek kuyruğu, mesaj kuyrukları
  (Büyük Veri patikasındaki Kafka benzetimi bir kuyruk).
- **Genişlik öncelikli arama (BFS):** bir graf ya da ağaçta yakından uzağa
  katman katman gezmek. Ağaçlar bölümünde ve ALG 2'nin graf bölümlerinde bu
  kuyrukla yapılacak.
- **Son `k` olay:** `deque(maxlen=k)` (kayan pencere bölümünde gördük).

## Özet

- Yığın: LIFO; Python'da liste (`append`, `pop`, `stack[-1]`), hepsi `O(1)`.
- Kuyruk: FIFO; Python'da `collections.deque` (`append`, `popleft`), `O(1)`.
  Listeyle `pop(0)` `O(n)`.
- Yığın kalıpları: geri alma, parantez denetimi, postfix hesaplama, çağrı
  yığını, monoton yığın (sıradaki büyük/küçük eleman `O(n)`).
- Kuyruk kalıpları: sırayla işlem, BFS, son `k` olay.
