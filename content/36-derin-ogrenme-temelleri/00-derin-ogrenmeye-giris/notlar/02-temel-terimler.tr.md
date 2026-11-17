Modül boyunca sık geçecek kelimeler. Her birini ilgili bölümde ayrıntılı
göreceğiz; burada kısa tanımları bir arada dursun.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Tensör (tensor)</span><span>PyTorch'un çok boyutlu sayı dizisi; NumPy dizisine benzer, türev de taşıyabilir.</span></div>
    <div class="anat-row"><span>Katman (layer)</span><span>Girdiyi bir çıktıya çeviren yapı taşı; <code>nn.Linear</code> gibi.</span></div>
    <div class="anat-row"><span>Parametre</span><span>Eğitimle ayarlanan sayılar: ağırlıklar ve sabitler (bias).</span></div>
    <div class="anat-row"><span>İleri hesap (forward pass)</span><span>Girdiyi katmanlardan geçirip çıktıyı hesaplamak.</span></div>
    <div class="anat-row"><span>Kayıp (loss)</span><span>Tahminin ne kadar yanlış olduğunu tek sayıyla ölçen fonksiyon.</span></div>
    <div class="anat-row"><span>Gradyan (gradient)</span><span>Kaybın her parametreye göre türevi: parametre biraz artınca kayıp ne yöne gider.</span></div>
    <div class="anat-row"><span>Geri yayılım (backpropagation)</span><span>Gradyanları zincir kuralıyla sondan başa doğru hesaplamak; PyTorch'ta <code>backward()</code>.</span></div>
    <div class="anat-row"><span>Optimizer</span><span>Gradyanlara bakıp parametreleri güncelleyen algoritma; <code>SGD</code>, <code>Adam</code>.</span></div>
    <div class="anat-row"><span>Öğrenme oranı (learning rate)</span><span>Her güncellemede ne kadar ilerleneceği.</span></div>
    <div class="anat-row"><span>Tur (epoch)</span><span>Eğitim verisinin tamamının bir kez kullanılması.</span></div>
    <div class="anat-row"><span>Küme (batch)</span><span>Bir güncellemede birlikte kullanılan örnekler; küçüğüne mini-batch denir.</span></div>
  </div>
  <figcaption>Modülün temel kelimeleri.</figcaption>
</figure>

"Derin" kelimesi katman sayısından geliyor: girdi ile çıktı arasında birden
çok katman olan ağa derin ağ deniyor. Dersteki ağın bir gizli katmanı var;
ileride katman ekledikçe aynı dört adımlı eğitim hiç değişmeyecek.
