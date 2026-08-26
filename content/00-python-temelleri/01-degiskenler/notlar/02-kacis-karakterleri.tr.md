Metnin içine doğrudan yazılamayan karakterler için **kaçış karakteri** kullanılır. Hepsi ters eğik çizgi ile başlar.

## En sık kullanılanlar

| Yazılışı | Ne yapar |
|---|---|
| `\n` | alt satıra geçer |
| `\t` | sekme boşluğu bırakır |
| `\\` | ters eğik çizginin kendisini yazar |
| `\'` | tek tırnak yazar |
| `\"` | çift tırnak yazar |

## Neden gerekiyor?

Bir metni tek tırnakla açtıysan, içindeki tek tırnak metni erken bitirir:

```python
hata = 'Alican'ın arabası'
```

Python `'Alican'` kısmını metin sanar, kalanını anlamlandıramaz ve `SyntaxError` verir. İki çözümü var:

```python
dogru1 = 'Alican\'ın arabası'    # tırnağı kaçır
dogru2 = "Alican'ın arabası"     # dış tırnağı çift yap
```

İkincisi genelde daha okunaklıdır. Kaçış karakterini ancak başka çare kalmadığında kullan.

## Satır atlatma

```python
print("Birinci satır\nİkinci satır")
```

Çıktı:

```
Birinci satır
İkinci satır
```

## Kaçışı kapatmak

Dosya yolu yazarken ters eğik çizgiler sorun çıkarır çünkü Python onları kaçış karakteri sanar. Metnin önüne `r` koyarsan kaçış işlemi tamamen kapanır:

```python
yol = r"C:\Users\yeni\belgeler"
```

`r` olmasaydı `\U`, `\y` ve `\b` kaçış karakteri olarak yorumlanır ve yol bozulurdu. Buna **ham metin** (raw string) denir; dosya yollarında ve düzenli ifadelerde çok işine yarayacak.
