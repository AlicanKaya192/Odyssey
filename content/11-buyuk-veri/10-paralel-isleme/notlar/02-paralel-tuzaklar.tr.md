Paralel kod sıralı koddan daha çok yerden bozulabiliyor. Bu sayfadaki her
hata bu makinede alındı.

## 1. `if __name__ == "__main__":` yok

Windows'ta her yeni süreç dosyayı baştan çalıştırıyor; korumasız havuz yeni
havuzlar kuruyor. Odyssey'de kod zaman aşımına uğradı. Havuzu kuran her
satır bu bloğun altında olmalı.

## 2. Süreç havuzuna `lambda` vermek

```python
ex.map(lambda x: x * 2, range(4))
# PicklingError: Can't pickle <function <lambda> ...>
```

Süreçlere giden fonksiyon kopyalanabilmeli (*pickle*); `lambda` buna uygun
değil. Dosyanın en dış düzeyinde `def` ile adlı bir fonksiyon yaz. İş
parçacığı havuzunda `lambda` sorun değil, çünkü kopyalama yok.

## 3. Fonksiyonu `if __name__` bloğunun içinde tanımlamak

```python
if __name__ == "__main__":
    def double(x):
        return x * 2
    ex.map(double, ...)
# BrokenProcessPool: A process in the process pool was terminated abruptly ...
```

Yardımcı süreçler bu bloğu çalıştırmıyor; fonksiyonu hiç görmüyorlar.
Fonksiyonlar bloğun **dışında** tanımlanır.

## 4. Süreçlerin bir değişkeni değiştirmesini beklemek

```python
counter = 0
def add(x):
    global counter
    counter += x
```

Dört süreçle `add`'i 0–9 için çağırınca ana programdaki `counter` **0**
kaldı: her süreç kendi kopyasını değiştirdi. İş parçacıklarıyla aynı kod 45
verdi (bellek ortak). Süreçlerden sonuç almak için fonksiyon değer
**döndürmeli**.

## 5. `as_completed`'tan sıra beklemek

`map` sonuçları verdiğin sırayla getiriyor (`[0, 1, 2, 3, 4]`);
`as_completed` hangisi önce biterse (`[4, 3, 2, 1, 0]`). Sıra önemliyse
`map` ya da sonuçları anahtarla eşle.

## 6. Her öğeyi ayrı göndermek

On bin küçük iş dört sürece tek tek gönderilince 0,0009 sn'lik iş 1,78 sn
sürdü. `chunksize` ver ya da paralel yapma.

## 7. Çekirdekten çok işçi açmak

Saf Python hesabında çekirdek sayısından fazla süreç açmak hızlandırmıyor;
süreçler sırayla çekirdek bekliyor. Bekleme işlerinde ise iş parçacığı
sayısı çekirdek sayısından çok olabilir.

## 8. Sonucu denetlememek

Paralel ve sıralı çözümün sonucu aynı olmalı. Bu patikadaki her paralel
örnekte iki sonuç karşılaştırıldı.
