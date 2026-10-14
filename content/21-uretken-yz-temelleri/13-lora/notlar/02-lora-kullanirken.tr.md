**Ne zaman LoRA?**

- Model büyük ve bütün ağırlıklarını güncellemek pahalıysa.
- Aynı modelin birçok görev için ayrı uyarlaması gerekiyorsa (her görev
  için yalnızca adaptör saklanır).
- Ön eğitimli modelin davranışını bozmadan geri dönülebilir bir değişiklik
  isteniyorsa.

**Seçimler:**

| Seçim | Etkisi |
|---|---|
| r (rank) | Küçük r az parametre; çok küçükse yetmez. Bölümde r = 1 %87, r = 4 %94 |
| Hangi katmanlar | Genellikle dikkat ve ileri katmanların ağırlıkları; ne kadar çok katman, o kadar çok parametre |
| Öğrenme oranı | Adaptör küçük olduğu için tam ince ayardan farklı bir oran gerekebilir |
| Başlangıç | B = 0: eğitim ön eğitimli modelden başlar |

**Adım adım:**

1. Önce yalnızca son katmanla ya da prompt'la dene; yetmiyorsa LoRA.
2. Küçük bir r ile başla (4–8), değerlendirme kümesinde ölç.
3. r'yi büyütmek doğruluğu artırmıyorsa dur.
4. Eski görevleri de ölç: LoRA ön eğitimli modeli değiştirmez ama
   birleştirilmiş model eski görevi kötüleştirebilir.

**Sık hatalar:**

- **B'yi rastgele başlatmak:** eğitim başında model ön eğitimli modelden
  uzaklaşır.
- **Türevleri güncellemeden sonra hesaplamak:** `g_A` ve `g_B` aynı `A` ve
  `B` ile hesaplanmalı.
- **Tek bir tohumla karar vermek:** bölümde farklar bir puanın altındaydı ve
  yön değiştirdi.
