Aşağıda çalışan bir fonksiyon var ama ne beklediği belli değil:

```python
def repeat(text, count):
    return text * count
```

Bu alıştırmada davranışını **değiştirmeden** ne beklediğini yazacaksın.

**Yapman gerekenler:**

1. `repeat` fonksiyonuna belirtimleri ekle:
   - `text` bir metin (`str`)
   - `count` bir tam sayı (`int`)
   - fonksiyon geriye metin döndürüyor (`str`)

2. Fonksiyonu iki kez çağırıp sonucu yazdır:
   - `repeat("ab", 3)`
   - `repeat("-", 5)`

**Beklenen çıktı:**

```
ababab
-----
```

Fonksiyonun gövdesine dokunma; yalnızca imza satırı değişecek.

> Parametreler `:` ile, dönüş parantezden sonra `->` ile belirtiliyor.
