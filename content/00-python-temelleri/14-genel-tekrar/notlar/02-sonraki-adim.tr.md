Python Temelleri bitti. Bu not, "şimdi ne yapayım" sorusunun cevabı.

## Önce dürüst bir değerlendirme

Bölümleri bitirmek, öğrenmiş olmak demek değil. Şunları **bakmadan**
yapabiliyor musun?

- Bir listedeki sayıların ortalamasını almak
- Bir sözlükte dolaşıp koşula uyanları toplamak
- İki değer alıp bir değer döndüren fonksiyon yazmak
- Bir dosyayı satır satır okuyup sözlüğe çevirmek
- `try` / `except` ile bozuk veriyi atlamak
- `__init__` ve bir metodu olan sınıf yazmak

Bir tanesinde takılıyorsan o bölüme geri dön. Utanılacak bir şey değil —
temel eksik kalırsa üstüne konan her şey sallanıyor.

## Hata mesajı okumak

Bundan sonra en çok yapacağın şey bu. Yöntemi:

1. **En alt satırı oku.** Hatanın türü ve açıklaması orada.
2. **Yukarı doğru bak.** Hangi dosyanın hangi satırında olduğunu bul.
3. **Kendi kodunun geçtiği en alt satıra odaklan.** Kütüphane içindeki
   satırlar genelde senin hatanın sonucu, sebebi değil.
4. **Hata metnini aynen ara.** Değişken adlarını çıkarıp aratmak sonucu
   iyileştiriyor.

Bir hatayı çözmek, yeni bir konu öğrenmekten daha çok şey öğretiyor.

## Nasıl pratik yapılır?

**Kendi işini otomatikleştir.** En iyi alıştırma, gerçekten ihtiyacın olan
şey. Örnekler:

- Bir klasördeki dosya adlarını düzenli hâle getiren betik
- Notlarını bir dosyada tutup arayan küçük program
- Ders programını okuyup "bugün ne var" diyen betik

**Küçük başla ve bitir.** Yarım kalan büyük proje, biten küçük projeden daha
az öğretiyor.

**Kendi kodunu bir hafta sonra oku.** Anlamıyorsan, yazarken yeterince açık
yazmamışsın demektir. Bu, en dürüst geri bildirim.

## Öğrenme yolunda sırada ne var?

<figure class="fig">
  <div class="flow">
    <span class="node ok"><b>Python</b><br>bitti</span>
    <span class="arrow">→</span>
    <span class="node acc"><b>Veri Bilimi</b><br>sıradaki</span>
    <span class="arrow">→</span>
    <span class="node"><b>Makine Öğrenmesi</b></span>
  </div>
  <figcaption>SQL, API ve Docker bu sıraya bağlı değil; Python bittikten sonra istediğin zaman girilebiliyor.</figcaption>
</figure>

**Veri Bilimi** doğal devam. Buradaki hangi bilgi oraya bağlanıyor:

| Burada öğrendiğin | Orada karşılığı |
|---|---|
| Liste | NumPy dizisi |
| Sözlük listesi | pandas tablosu (`DataFrame`) |
| Dosya okuyup ayrıştırmak | `read_csv` |
| Döngüyle süzmek | Tablo süzme |
| `dict[str, list[int]]` okumak | Tablo sütunlarını anlamak |

**SQL** bu bölümde başladığın yerden devam ediyor: `SELECT` ve `WHERE`
biliyorsun, oraya `JOIN` ekleniyor.

**API** için sözlük ve hata yakalama bilgin şart — API cevapları JSON gelir,
JSON da Python'da sözlüktür.

## Sık sorulan: "Kütüphane varken bunları neden öğrendim?"

pandas `read_csv` ile bir satırda dosya okuyor. Sen on satır yazdın. Boşa mı
gitti?

Hayır. Şu üç durumda fark ortaya çıkıyor:

- **Dosya bozuk bir satır içerdiğinde.** `read_csv` hata veriyor ve ne
  olduğunu yalnızca elle ayrıştırmayı bilen anlıyor.
- **Kütüphanenin yapmadığı bir şey gerektiğinde.** O zaman kendin yazman
  gerekiyor.
- **Hata mesajını okurken.** `KeyError` ne demek, `NoneType` neden çıkıyor —
  bunlar dilin bilgisi, kütüphanenin değil.

Kütüphane sana hız veriyor, temel sana **kontrol** veriyor.

## Bir tavsiye

Yeni bir şey öğrenirken önce **ne işe yaradığını** anla, sonra nasıl
yazıldığını. Sözdizimi aratılabiliyor; ne zaman kullanılacağı aratılamıyor.

Bu bölümlerde her konunun başında "sorun ne?" diye bir kısım olmasının sebebi
de bu.
