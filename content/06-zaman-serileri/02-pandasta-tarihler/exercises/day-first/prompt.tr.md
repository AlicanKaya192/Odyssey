`orders.csv` dosyasında sipariş zamanı gün önde yazılmış:
`03.01.2024 05:12`. Önce tuzağı kendi gözünle gör, sonra dosyayı doğru oku.

**Yapman gerekenler:**

1. Şu küçük seriyi **biçim yazmadan** tarihe çevir ve ay numaralarını liste
   olarak yazdır (`.dt.month.tolist()`):

   ```python
   sample = pd.Series(["09.03.2024", "10.03.2024", "11.03.2024"])
   ```

2. Aynı seriyi `format="%d.%m.%Y"` ile çevir ve ay numaralarını yazdır.
3. `orders.csv` dosyasını oku; `ordered_at` sütununu
   `format="%d.%m.%Y %H:%M"` ile çevir.
4. İlk ve son sipariş zamanını aynı satıra yazdır.
5. Aylara göre sipariş sayısını yazdır:
   `ordered.dt.month.value_counts().sort_index().to_dict()`.

**Beklenen çıktı:**

```
[9, 10, 11]
[3, 3, 3]
2024-01-03 05:12:00 2024-04-30 20:47:00
{1: 51, 2: 62, 3: 65, 4: 59}
```

İlk satır tuzak: üçü de Mart'tı ama biçimsiz okununca Eylül, Ekim ve Kasım
oldu; hata da uyarı da çıkmadı. Son satır bir sağlama: siparişler Ocak–Nisan
arasında, dört aya yayılmış. Sonuç on iki aya dağılsaydı gün ile ay yer
değiştirmiş olurdu.
