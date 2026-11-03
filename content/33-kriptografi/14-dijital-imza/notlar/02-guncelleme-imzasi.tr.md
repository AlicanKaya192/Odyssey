Yazılım güncellemesi imzanın en tanıdık kullanımıdır: program, indirdiği
dosyanın gerçekten üreticiden geldiğini ve yolda değişmediğini imzayla
anlar.

<figure class="fig">
<div class="flow">
<span class="node">Üretici paketi imzalar</span>
<span class="arrow">→</span>
<span class="node">Paket + imza indirilir</span>
<span class="arrow">→</span>
<span class="node acc">Gömülü açık anahtarla doğrula</span>
<span class="arrow">→</span>
<span class="node acc">Sürüm eskisinden yeni mi?</span>
<span class="arrow">→</span>
<span class="node ok">Kur</span>
</div>
<figcaption>Güvenli güncelleme: imza tutmazsa ya da sürüm geriye gidiyorsa kurulum yapılmaz.</figcaption>
</figure>

## Neden açık anahtar programın içinde

Doğrulama anahtarı güncellemeyle birlikte indirilseydi, paketi değiştiren
biri anahtarı da değiştirebilirdi. Anahtar programa önceden gömülür ya da
işletim sisteminin güvendiği bir sertifika zincirinden gelir.

## Neden sürüm de denetlenir

Eski bir sürüm de üretici tarafından **geçerli şekilde** imzalanmıştır.
Bilinen bir açığı olan eski sürümü "güncelleme" diye sunmak imza
denetimini geçer. Bu yüzden imzalı bilgiye sürüm numarası konur ve program
**geriye giden** sürümü kurmaz.

## İmzanın korumadığı

- Üreticinin kendi derleme makinesine giren zararlı kod da imzalanır;
  imza "üretici imzaladı" der, "kod zararsız" demez.
- Özel anahtar çalınırsa saldırgan geçerli imza atabilir. Bu yüzden imza
  anahtarı ayrı, korumalı bir yerde (donanım güvenlik modülü gibi) tutulur
  ve gerekirse iptal edilebilir olmalıdır.
