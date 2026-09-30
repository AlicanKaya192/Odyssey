`store_sales.csv` dosyasındaki `date` sütunu metin olarak geliyor. Onu
gerçek tarihe çevir ve sütunun artık takvimi bildiğini göster.

**Yapman gerekenler:**

1. Dosyayı oku ve `date` sütununu `pd.to_datetime` ile çevir.
2. Çevirmenin tuttuğunu doğrula:
   `pd.api.types.is_datetime64_any_dtype(sales["date"])` sonucunu yazdır.
3. En erken ve en geç tarihi `"%Y-%m-%d"` biçiminde aynı satıra yazdır.
4. İkisi arasındaki gün sayısını yazdır.
5. İlk tarihin gün adını (`day_name()`) yazdır.

**Beklenen çıktı:**

```
True
2022-01-01 2024-12-31
1095
Saturday
```

Üç yıl 1096 gün, ama ilk ile son gün arası 1095: aradaki **adım** sayısı,
gün sayısından bir eksik.
