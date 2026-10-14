| Adım | Ne yapar? | Bölüm | Ölçüsü |
|---|---|---|---|
| Maskele | Kişisel veriyi soru aramaya ve kayda gitmeden gizler | 14 | Örnek cümlelerde yakalanan / kaçan |
| Ara | En ilgili makaleyi, sonra cümlelerini bulur | 09 | key@k, recall@k, MRR |
| Bütçeye sığdır | Kaynakları token sınırında tutar | 07 | Soru başına token, maliyet |
| Prompt kur | Numaralı kaynaklar + kurallar + soru | 10 | — |
| Cevap al | Model (burada örnek okuyucu) | 06, 10 | Doğru, yanlış, kaçırılan |
| Doğrula | Kaynak numarası ve sayılar | 08 | Yakalanan uydurma |
| Kaydet | Maskelenmiş soru, sonuç, token, maliyet | 07 | Kullanım özeti |
| Ölç | Değerlendirme kümesiyle karşılaştır | 11 | Gruplar, aralık |

**Akılda tut:**

- Bölümde iki aşamalı arama yanlış cevapları 2'den 0'a indirdi; kaçırma
  7'den 9'a çıktı, token 132'den 154'e.
- Doğrulama, kaynakta olmayan "5 years"ı yakaladı.
- Her adımın kendi ölçüsü var; sistem bunlarla iyileştirilir.
