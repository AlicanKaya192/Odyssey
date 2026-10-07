pandas bilen biri dask'ta çoğu şeyi hemen yazabiliyor; takıldığı yerler
genellikle bunlar.

## 1. Sonuç gelmiyor, "yapı" geliyor

`print(ddf)` ya da `print(ddf["unit_price"].mean())` değer değil, tarif
yazdırıyor. Değer için `.compute()`.

## 2. `compute`'u döngünün içinde çağırmak

```python
for city in cities:
    # her turda dosyalar yeniden okunuyor
    ddf[ddf["city"] == city]["unit_price"].mean().compute()
```

Her `compute` tarifi baştan çalıştırıyor. Hepsini tek bir `groupby` ile ya
da tarifleri toplayıp tek `dask.compute(...)` ile hesapla.

## 3. Kesin ortanca yok

`median()` `NotImplementedError` verdi; `quantile(0.5)` yaklaşık sonuç
(449,72; gerçek 449,05). Kesin ortanca şartsa DuckDB'nin `median` işlevi ya
da verinin tamamı.

## 4. Sıralamak ve indeks değiştirmek pahalı

`sort_values` ve `set_index` verinin bölümler arasında yer değiştirmesini
gerektiriyor. Çoğu analizde gerekmiyor; gerekirse bir kez yap ve sonucu
Parquet olarak sakla.

## 5. `dask.bag` süreç kullanıyor

Varsayılan zamanlayıcısı süreçler; `if __name__ == "__main__":` olmadan
Windows'ta `RuntimeError` / `BrokenProcessPool` (denendi).

## 6. Sonuç belleğe sığmayabilir

`compute()` sonucu pandas nesnesi olarak belleğe getiriyor. Süzülmüş büyük
bir tablo `compute` edilirse bellek yine dolar. Büyük sonucu belleğe almadan
yaz: `ddf.to_parquet("out/")`.

## 7. Bölüm sayısını düşünmemek

Çok küçük bölümler hazırlık işini çoğaltıyor, çok büyükler belleğe sığmıyor.
dask belgeleri bölüm başına kabaca yüz megabayt öneriyor.

## 8. Küçük veride dask

Veri belleğe rahatça sığıyorsa dask'ın görev grafiği yalnızca ek iş. Bu
patikanın ölçümünde sırayla çalışan dask pandas kadar sürdü; kazanç
çekirdeklerden ve bellekten geliyor.
