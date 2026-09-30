Aynı ayrıştırmayı `seasonal_decompose` ile yap, grafiğini kaydet ve
kalıntıyı sorgula.

**Yapman gerekenler:**

1. `result = seasonal_decompose(s, model="additive", period=7)`.
2. Dört panelli grafiği kaydet: `fig = result.plot()`, sonra
   `fig.savefig("chart.png")`.
3. Kalıntıdaki `NaN` sayısını ve kalıntının standart sapmasını (iki ondalık)
   aynı satıra yazdır.
4. Mutlak değeri en büyük üç kalıntının tarihlerini liste olarak yazdır
   (`"%Y-%m-%d"`).
5. En büyük kalıntının günü için gözlemi, trendi, mevsimi ve kalıntıyı (bir
   ondalık) aynı satıra yazdır.
6. Kalıntının haftanın gününe göre ortalamasının mutlak değerce en büyüğünü
   bir ondalığa yuvarlayıp yazdır.
7. **Trend** bileşeninin aya göre ortalamasını al; en düşük ve en yüksek ayın
   numarasını ve değerini (tam sayı) `ay değer ay değer` biçiminde yazdır.

**Beklenen çıktı:**

```
6 12.32
['2023-12-30', '2024-11-09', '2022-05-14']
462 338.3 76.2 47.5
0.0
6 231 12 322
```

Kalıntının haftanın gününe göre ortalaması sıfır: haftalık desen tamamen
ayrılmış. Ama trendin kendisi Haziran'dan Aralık'a 90 birim oynuyor: yıllık
mevsim ayrılmadı, trendin içinde duruyor. Sol taraftaki **Çıktı** sekmesinde
trend panelinin yılda bir dalga çizdiğini göreceksin.
