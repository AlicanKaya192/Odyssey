Aynı hesabı iki yolla yap ve `tracemalloc` ile tepe belleği ölç.

Hesap: 2 milyon fiyatın her birine %20 vergi ekle ve sonucu iki ondalığa
yuvarla.

**Yapman gerekenler:**

1. **Birinci yol** (her adım yeni dizi):
   - `tracemalloc.start()`
   - `prices = np.ones(2_000_000)`
   - `taxed = prices * 1.2`
   - `final = np.round(taxed, 2)`
   - Tepeyi al, `tracemalloc.stop()`.
2. **İkinci yol** (aynı dizinin üstünde, *yerinde*):
   - `tracemalloc.start()`
   - `prices = np.ones(2_000_000)`
   - `prices *= 1.2`
   - `np.round(prices, 2, out=prices)`
   - Tepeyi al, `tracemalloc.stop()`.
3. İki tepeyi MB olarak bir ondalığa yuvarlayıp ayrı satırlara yazdır.
4. Son satıra birinci tepenin ikinciye oranını tam sayıya yuvarlayıp
   yazdır.

`prices *= 1.2` yeni dizi kurmadan diziyi kendi üstünde değiştiriyor;
`out=prices` de sonucun aynı diziye yazılmasını söylüyor.

**Beklenen çıktı:**

```
45.8
15.3
3
```

Sonuç aynı ama birinci yol bellekte aynı anda üç dizi tutuyor.
