Bir kart son 120 saniyede toplam 1000'den fazla harcadığında uyar.

**Yapman gerekenler:**

1. Her kart için son ödemeleri `(ts, amount)` olarak bir `deque`'de ve
   pencerenin toplamını ayrı bir sözlükte tut.
2. Her ödemede: ödemeyi ekle, toplama ekle; `ts`'si `event["ts"] - 120`
   ya da daha eski olanları soldan çıkar ve toplamdan düş.
3. **Eşik aşıldığı anda bir kez** uyar: ödemeden önceki toplam 1000 ya da
   altındaydı, şimdi 1000'den büyük.
4. `payments(20_000)` için ilk üç uyarıyı `event_id kart toplam` (toplam
   iki ondalık) yazdır, sonra uyarı sayısını yazdır.

**Beklenen çıktı:**

```
708 C086 1016.64
869 C053 1057.89
1331 C183 1002.36
70
```
