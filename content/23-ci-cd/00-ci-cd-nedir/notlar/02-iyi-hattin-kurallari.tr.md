Bir hattın işe yaraması yalnızca dosyanın doğru yazılmasına değil, ekibin
onunla nasıl çalıştığına da bağlı. Sık duyulan kurallar:

1. **Küçük değişiklik, sık birleştirme.** İki haftalık değişiklik
   kırmızı olduğunda sorunu bulmak zordur; yirmi satırlık değişiklikte
   kolaydır.
2. **Ana dal kırmızıysa önce o düzeltilir.** Kırmızı dalın üstüne iş
   eklemek, bir sonraki hatanın hangi değişiklikten geldiğini gizler.
3. **Hızlı aşamalar önde.** Biçim denetimi saniyeler sürer, uzun testler
   dakikalar. Ucuz kapı önce kapanırsa pahalı olana hiç gelinmez.
4. **Hat hızlı kalsın.** Sonuç on dakikadan uzun sürerse insanlar
   beklemeyi bırakır ve hat bir alışkanlık olmaktan çıkar. Önbellek ve
   paralel işler bunun için var (ilerideki bölümlerde).
5. **Yerelde de çalıştır.** Hat, testi senin yerine çalıştırmaz; senin
   bilgisayarında atladığın bir sorunu yakalar. Göndermeden önce testleri
   kendin de çalıştır.
6. **Temiz makineyi unutma.** Çalıştırıcıda hiçbir şey hazır değildir:
   ilk adım kodu indirmek (`actions/checkout`), sonra Python'u ve
   bağımlılıkları kurmak.
7. **Eylemlerin sürümünü yaz.** `actions/checkout@v4` yazılır,
   `actions/checkout` değil. Sürümsüz eylemi GitHub kabul etmez; sürüm,
   eylem değişse bile hattın aynı kalmasını sağlar.

**Sık görülen belirti → olası neden**

| Belirti | Olası neden |
|---|---|
| `requirements.txt` bulunamadı | Kodu indiren adım (`checkout`) yok. |
| Bende geçiyor, hatta düşüyor | Bir paket yalnızca senin bilgisayarında kurulu. |
| Hat 20 dakika sürüyor | Yavaş aşamalar önde, önbellek yok. |
| Hat yeşil ama program bozuk | Bozulan şeyin testi yok. |
