Berlin'deki bir sensör saatte bir sıcaklık kaydediyor; zaman damgaları
UTC (`2024-03-29T23:00:00Z`). Rapor ise yerel güne göre isteniyor.

**Yapman gerekenler:**

1. `berlin_sensor.csv` dosyasını oku ve `time_utc` sütununu tarihe çevir.
2. `dt.tz_convert("Europe/Berlin")` ile yerel saate çevirip `local` adlı
   sütuna yaz.
3. Her **yerel gün** için kaç kayıt olduğunu yazdır: `local.dt.date`
   üzerinde `value_counts().sort_index()`; her günü `tarih sayı` biçiminde
   bir satıra.
4. En yüksek sıcaklığın ölçüldüğü satırın **yerel** zamanını
   `"%Y-%m-%d %H:%M"` biçiminde yazdır (`idxmax()`).

**Beklenen çıktı:**

```
2024-03-30 24
2024-03-31 23
2024-04-01 24
2024-03-31 12:00
```

UTC'de hiçbir saat eksik değil. 31 Mart'ın 23 satır olması, o gece Berlin'in
saatleri bir saat ileri almasından. Günlük toplam alan bir rapor o günü
olduğundan düşük gösterirdi.
