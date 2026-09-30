`web_traffic.csv` bir sitenin günlük ziyaret sayısı. İçinde iki kampanya
sıçraması, bir kesinti ve 2 Eylül'den itibaren kalıcı bir seviye artışı var.
Bunları grafiğe işle.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `visits` sütununu `visits` serisine al.
2. Olağandışı günleri bul (Bölüm 07'deki yöntem):
   `base = visits.shift(1).rolling(28)`,
   `z = (visits - base.mean()) / base.std()`, `unusual = z[z.abs() > 3]`.
3. Seriyi `figsize=(10, 4)` tuvalde çiz.
4. Her olağandışı gün için bir dikey kesik çizgi ekle
   (`ax.axvline(day, linestyle="--", color="gray")`).
5. 2 Eylül 2024'ten serinin sonuna kadar olan dönemi gölgele
   (`ax.axvspan(..., alpha=0.15)`) ve `chart.png` olarak kaydet.
6. İşaretlenen günleri `"%m-%d"` biçiminde liste olarak yazdır.
7. Grafikteki çizgi sayısını yazdır (`len(ax.lines)`).
8. 2 Eylül'den önceki ve sonraki dönemin ortanca ziyaretini tam sayıya
   yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
['03-14', '06-20', '10-08']
4
3917 5129
```

Çizgi sayısı dört: serinin kendisi ve üç dikey işaret. Gölgeli alan olmadan
2 Eylül'deki değişim kademeli bir büyüme gibi okunabilirdi; ortancalar bunun
tek seferde olan bir seviye değişimi olduğunu gösteriyor.
