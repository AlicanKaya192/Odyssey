Dedektörün eşiğini bakım defterindeki 12 olaya karşı sına: kesinlik ve
duyarlılık.

Başlangıç kodunda `score` (saat profilinden dayanıklı puan) ve `events` hazır.

**Yapman gerekenler:**

1. `evaluate(threshold, skip)` fonksiyonunu yaz:
   - `skip` içindeki saatleri puandan çıkar (`score.drop(skip)`)
   - mutlak puanı eşiği geçen saatleri bul
   - dört değeri demet olarak döndür: alarm sayısı, bunların `events` içinde
     olan sayısı, kesinlik (doğru / alarm) ve duyarlılık (doğru / olay sayısı);
     oranlar iki ondalık.
2. Hiçbir şey atlamadan (`skip=[]`) eşik 3 için sonucu yazdır.
3. Takılı sensör saatlerini ayır:
   `stuck = pd.date_range("2024-09-30 08:00", "2024-09-30 16:00", freq="h")`.
   Eşik 2, 2.5, 3, 4 ve 6 için `skip=stuck` ile sonucu eşikle birlikte alt alta
   yazdır.
4. Eşik 4 iken kaçan olayları `"%m-%d %H"` listesi olarak yazdır.

**Beklenen çıktı:**

```
(20, 12, 0.6, 1.0)
2 (38, 12, 0.32, 1.0)
2.5 (16, 12, 0.75, 1.0)
3 (12, 12, 1.0, 1.0)
4 (10, 10, 1.0, 0.83)
6 (8, 8, 1.0, 0.67)
['09-28 19', '10-04 12']
```

İlk satırda kesinlik 0.6 görünüyor: 20 alarmın 8'i defterde yok. Ama o sekizi
takılı sensör: gerçek bir sorun, yalnızca deftere yazılmamış. Ayrılınca eşik 3
kusursuz. Eşik düştükçe yanlış alarm çoğalıyor (eşik 2'de 26), yükseldikçe
küçük olaylar kaçıyor. "Yanlış alarm" demeden önce alarmın neye denk geldiğine
bak: etiketler de eksik olabilir.
