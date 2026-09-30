On iki alarmı olaylara çevir: birbirine yakın alarmları birleştir, yönüne ve
uzunluğuna bakarak her olayı adlandır.

Başlangıç kodunda `deviation` (oransal sapma) ve `alarm` (doğru/yanlış) hazır.

**Yapman gerekenler:**

1. Alarm günlerini al: `days = alarm[alarm].index`.
2. Günleri olaylara ayır: bir alarm, bir öncekinden **en çok 3 gün** sonraysa
   aynı olaya aittir; değilse yeni bir olay başlar. Her olay bir gün listesi.
3. Her olay için bir satır yazdır:
   - ilk ve son gün (`"%m-%d"`)
   - alarm sayısı
   - yön: sapmaların hepsi artıysa `up`, hepsi eksiyse `down`, değilse `mixed`
   - tür: alarm sayısı 3 ve üzeriyse `shift`, değilse `spike`

**Beklenen çıktı:**

```
03-14 03-14 1 up spike
06-20 06-20 1 up spike
09-02 09-14 9 up shift
10-08 10-08 1 down spike
```

On iki alarm dört olaya indi. Üçü tek günlük sıçrama; biri dokuz alarmlık,
hep aynı yönde bir dizi: düzey kayması. Bir izleme ekranında on iki ayrı
bildirim yerine bu dört satır gösterilir.
