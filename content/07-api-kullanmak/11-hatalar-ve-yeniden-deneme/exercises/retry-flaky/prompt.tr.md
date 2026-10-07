`/flaky` ilk iki istekte `503` (meşgul) veriyor, sonra cevap veriyor.

**Yapman gerekenler:**

1. En fazla 5 deneme yapan bir döngü kur. Her denemede `timeout=5` ile
   istek gönder, deneme numarasını ve durum kodunu yazdır.
2. `200` gelince döngüden çık; gelmezse bir sonraki denemeden önce **1
   saniye bekle** (`time.sleep(1)`).
3. Sonda raporun içindeki `report` ve `attempt` değerlerini yazdır.

**Beklenen çıktı:**

```
attempt 1 503
attempt 2 503
attempt 3 200
report: ready
after attempt: 3
```

Kontrol, istekler arasında gerçekten beklediğine de bakıyor.
