Durum satırı üç parça: sürüm, kod ve açıklama. Ama dikkat: açıklamanın
kendisinde de boşluk olabilir (`Not Found`, `Too Many Requests`). Basit bir
`split(" ")` açıklamayı parçalara böler.

**Yapman gerekenler:**

1. `parse_status_line(line)` fonksiyonunu yaz:
   `{"version": ..., "code": ..., "reason": ...}` döndürsün. `code` **sayı**
   (int) olsun. En fazla iki kez böl: `line.split(" ", 2)`.
2. `lines` listesindeki her satır için kodu ve açıklamayı aşağıdaki gibi
   yazdır; sonunda başarılı olanların sayısını yaz.

**Beklenen çıktı:**

```
200 | OK
404 | Not Found
429 | Too Many Requests
201 | Created
successful: 2
```
