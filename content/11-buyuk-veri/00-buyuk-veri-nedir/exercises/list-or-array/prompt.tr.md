Aynı 100 000 ondalıklı sayıyı bir Python listesinde ve bir NumPy
dizisinde sakla; ikisinin boyutunu ölç.

**Yapman gerekenler:**

1. `values = [i * 0.5 for i in range(100_000)]` listesini kur.
2. `array = np.arange(100_000) * 0.5` dizisini kur.
3. Listenin gerçek boyutunu bayt olarak bul: listenin kendisi
   (`sys.getsizeof(values)`) **artı** içindeki her sayının boyutu.
4. Dizinin boyutunu `array.nbytes` ile bul.
5. İki boyutu MB olarak (bir ondalık) aynı satıra, altına da listenin
   diziden kaç kat büyük olduğunu (bir ondalık) yazdır.

**Beklenen çıktı:**

```
3.1 0.8
4.0
```

Ondalıklı sayı nesnesi 24 bayt, adresi 8 bayt; dizide ise her sayı 8 bayt.
