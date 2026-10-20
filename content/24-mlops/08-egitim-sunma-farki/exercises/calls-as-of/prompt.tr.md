Eğitim tablosunun her satırında bir müşteri ve bir etiket tarihi var (`labels`: `[müşteri, tarih]`). Destek aramaları ayrı bir listede (`calls`: `[müşteri, tarih]`). `calls_as_of(labels, calls)` fonksiyonunu yaz:

- Her etiket satırı için o müşterinin etiket tarihinden **önce** (aynı gün sayılmaz) yaptığı aramaları say.
- `[müşteri, tarih, sayı]` listelerini etiketlerin sırasıyla döndür.

Etiket tarihinde ve sonrasında yapılan aramalar tahmin anında bilinmiyordu; onları saymak zaman sızıntısı olurdu.

**Beklenen çıktı:**

```
['C1', '2026-02-15', 1]
['C2', '2026-02-15', 0]
['C1', '2026-03-10', 3]
```
