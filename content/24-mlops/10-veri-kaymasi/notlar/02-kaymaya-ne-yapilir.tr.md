Kayma ölçüldü. Şimdi ne olacak?

<figure class="fig">
  <div class="flow">
    <span class="node">Kayma uyarısı</span>
    <span class="arrow">→</span>
    <span class="node">Gürültü mü?</span>
    <span class="arrow">→</span>
    <span class="node">Önemli sütun mu?</span>
    <span class="arrow">→</span>
    <span class="node acc">Kalite düştü mü?</span>
  </div>
  <figcaption>Yeniden eğitme kararı son soruya göre verilir.</figcaption>
</figure>

## Sorular sırayla

1. **Gürültü mü?** Aynı dönemden başka bir örneklemin PSI'si ne kadar?
   Ölçülen kayma bunun belirgin üstünde mi?
2. **Veri hatası mı?** Kayma birden ve tek bir sütunda mı başladı? Bir
   birim değişikliği ya da bozuk bir kaynak olabilir (Veri Doğrulama).
3. **Önemli bir sütun mu?** Model bu sütuna ne kadar güveniyor?
4. **Kalite düştü mü?** Etiketler gelince doğruluk ölçülür. Düşmediyse
   kayma zararsız; izlemeye devam.
5. Düştüyse: yeni veriyle yeniden eğit, kapıdan geçir, kayda koy
   (Kavram Kayması ve Yeniden Eğitim).

## Kontrol listesi

- Referans veri belli ve kayıtta mı (hangi eğitim verisi)?
- Her sütun için gürültü düzeyi ölçüldü mü?
- Eşik büyüklük ölçüsüne (PSI, KS istatistiği) mi konuldu?
- Kategorik sütunların payları da izleniyor mu?

## Yapma

- Uyarıyı p-değerine bağlama.
- Her kaymada kendiliğinden yeniden eğitme; veri hatasını modele
  öğretmiş olabilirsin.
- PSI eşiklerini kanun sanma; kendi verinin gürültüsüne göre ayarla.
