Günlük satışta iki desen var: haftalık ve yıllık. Yalnızca haftalığı
ayıran klasik yöntemi, ikisini birden ayıran `MSTL` ile karşılaştır.

**Yapman gerekenler:**

1. `classic = seasonal_decompose(s, model="additive", period=7)`.
2. `fit = MSTL(s, periods=(7, 365)).fit()`.
3. `fit.seasonal` tablosunun sütunlarını liste olarak yazdır.
4. Kalıntının standart sapmasını klasik ve MSTL için iki ondalığa yuvarlayıp
   aynı satıra yazdır.
5. **Trend** bileşeninin aya göre ortalamasını iki yöntem için al; her birinde
   en yüksek ay ile en düşük ay arasındaki farkı tam sayıya yuvarlayıp aynı
   satıra yazdır (önce klasik).
6. MSTL trendinin ilk ve son değerini bir ondalığa yuvarlayıp aynı satıra
   yazdır.
7. Yıllık mevsim bileşeninin (`fit.seasonal["seasonal_365"]`) 2024'teki en
   yüksek ve en düşük gününü `"%m-%d"` biçiminde aynı satıra yazdır.

**Beklenen çıktı:**

```
['seasonal_7', 'seasonal_365']
12.32 5.89
91 32
207.4 310.7
12-30 06-11
```

Klasik yöntemde trend yıl içinde 90 birim oynuyordu: o oynama yıllık mevsimdi.
MSTL onu kendi sütununa aldı ve kalıntı yarıya indi. MSTL trendinde kalan 32
birimlik fark mevsim değil: mağaza yılda 35 birim kadar büyüyor, Aralık
ortalaması Ocak'ınkinden bu yüzden yüksek.
