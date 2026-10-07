Git satırlara bakar, anlama değil. Hangi durumda kendisinin birleştirdiğini,
hangisinde sorduğunu bilmek çakışmaları önceden görmeni sağlar.

| İki dal ne yaptı? | Sonuç |
|---|---|
| Farklı dosyaları değiştirdi | Kendiliğinden birleşir. |
| Aynı dosyanın birbirinden uzak satırlarını değiştirdi | Kendiliğinden birleşir (`Auto-merging`). |
| Aynı satırı aynı biçimde değiştirdi | Kendiliğinden birleşir; değişiklik bir kez yazılır. |
| Aynı satırı farklı değiştirdi | **Çakışma** (`CONFLICT (content)`). |
| Yan yana satırları değiştirdi | Çoğu zaman **çakışma**; Git aradaki sınırı bilemez. |
| Biri dosyayı sildi, öbürü değiştirdi | **Çakışma** (`CONFLICT (modify/delete)`). |
| İkisi de aynı adla yeni dosya ekledi, içerik farklı | **Çakışma** (`CONFLICT (add/add)`). |

## Git anlamı bilmez

Çakışmasız bir birleştirme her zaman **doğru** bir sonuç demek değil. Örneğin
bir dal bir fonksiyonun adını değiştirdi, öbürü eski adla yeni bir yerde
çağırdı: satırlar farklı, Git sorunsuz birleştirir ama program bozulur. Bu
yüzden birleştirmeden sonra programı çalıştırıp testleri koşmak gerekir;
ekipler bunu otomatik yapan araçlar (*CI*) kullanır.

## Aynı çakışmayı ikinci kez çözmemek

Uzun yaşayan bir dalı `main` ile sık birleştiriyorsan aynı çakışma tekrar
tekrar çıkabilir. Git'in `rerere` (*reuse recorded resolution*) ayarı bir
kez çözdüğün çakışmayı hatırlar ve bir dahakine kendisi uygular:

```text
git config --global rerere.enabled true
```

Başlangıç için gerekli değil; büyüyen projelerde işe yarar.
