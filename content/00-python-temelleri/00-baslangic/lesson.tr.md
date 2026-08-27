# Başlangıç

Bu bölüm Python'a ve bu uygulamaya kısa bir giriş. Kod yazmadan önce neyle uğraştığını bilmek işini kolaylaştırır.

## Python nedir?

Python, 1991 yılında Guido van Rossum tarafından geliştirilen bir programlama dilidir. Tasarlanırken tek bir şey öne alınmış: **okunabilirlik.**

Aynı işi yapan iki kod parçasına bakalım. Önce Java:

```java
public class Merhaba {
    public static void main(String[] args) {
        System.out.println("Merhaba");
    }
}
```

Sonra Python:

```python
print("Merhaba")
```

Bu fark, öğrenmeye yeni başlayan biri için ciddi bir avantaj. Dilin kurallarıyla boğuşmak yerine çözmeye çalıştığın problemle ilgilenebiliyorsun.

## Neden veri biliminde Python?

Üç sebebi var.

**Kütüphaneleri olgun.** NumPy sayısal hesaplama, pandas veri işleme, scikit-learn makine öğrenmesi için yıllardır geliştirilen araçlar. Bunları sıfırdan yazmak yıllar alırdı.

**Topluluğu geniş.** Karşılaştığın hemen her sorunun cevabı bir yerlerde var. Tıkandığında yalnız kalmıyorsun.

**Hem prototip hem üretim.** Bir fikri hızlıca deneyip, işe yaradığında aynı dille üretime alabiliyorsun.

## Yorumlanan bir dil

Python **yorumlanan** bir dildir: yazdığın kod satır satır çalıştırılır, önce derlenmesi gerekmez. Bu, hızlı deneme yapmayı kolaylaştırır — bir satır yaz, sonucunu hemen gör.

Karşılığında C veya Rust gibi derlenen dillere göre yavaştır. Ama veri biliminde ağır hesaplamayı zaten NumPy gibi kütüphaneler yapıyor ve onların çekirdeği C ile yazılmış. Pratikte bu yavaşlık çoğu zaman hissedilmiyor.

## print() — ilk komutun

Ekrana bir şey yazdırmanın yolu `print()`:

```python
print("Merhaba")
```

Parantezin içine yazdırmak istediğini koyarsın. Metinler tırnak içine alınır, sayılar alınmaz:

```python
print("Merhaba")   # metin  -> tırnak gerekli
print(42)          # sayı   -> tırnak yok
```

## Yorum satırları

`#` işaretinden sonrası Python tarafından hiç okunmaz. Bunlar kendine ya da kodu okuyacak kişiye not bırakmak içindir:

```python
# Bu satır çalışmaz, sadece açıklama
print("Bu çalışır")   # satır sonuna da yazılabilir
```

Bu uygulamadaki alıştırmalarda başlangıç kodunda yorum satırları göreceksin — ne yapman gerektiğini söylüyorlar.

## Bu uygulama nasıl çalışıyor?

Her bölüm dört parçadan oluşuyor:

**Konu Anlatımı** — şu an okuduğun sayfa. Sağdaki başlık listesinden istediğin yere atlayabilirsin.

**Ders Notları** — konuyu derinleştiren ek metinler. Ana anlatımı kısa tutup ayrıntıları oraya bıraktım.

**Sınav** — çoktan seçmeli sorular. Amacı not vermek değil; her sorunun altında neden o cevabın doğru olduğunu anlatan bir açıklama var.

**Alıştırma** — kod yazdığın yer. Yazdığın kodu çalıştırıp kontrol ediyor: çıktın doğru mu, doğru değişkeni tanımladın mı, istenen yapıyı kullandın mı.

## Alıştırmalar hakkında

Alıştırmalarda tıkanırsan **üç kademeli ipucu** var. İlki seni yönlendirir, ikincisi adım adım anlatır, üçüncüsü çözümü gösterir. Ne kadarını açacağına sen karar veriyorsun — hiçbiri kendiliğinden açılmıyor.

Kodun hata verirse, hatanın altında **ne anlama geldiğini** anlatan bir kutu çıkıyor. Python'un `TypeError` gibi mesajları doğru ama öğretmiyor; orada ne olduğunu ve nasıl düzelteceğini bulacaksın.

> **Değişken adları İngilizce.** Bu uygulamadaki bütün alıştırmalarda `team`, `total`, `score` gibi İngilizce adlar kullanılıyor. Sebebi ikili: gerçek Python kodu zaten böyle yazılır, ve uygulamayı İngilizce kullananların klavyesinde Türkçe karakterler yok.

## İlerleme

İlerlemen bilgisayarında saklanıyor. Bir bölümü tamamladığında yol ekranında işaretleniyor, uygulamayı kapatıp açtığında yazdığın kod olduğu yerde duruyor.

Bölümler kilitli değil — istediğin sıraya atlayabilir, tamamladığın bir bölüme geri dönüp tekrar okuyabilirsin.

---

## Özet

- Python okunabilirliği öne alan, yorumlanan bir dildir.
- Veri biliminde tercih edilmesinin sebebi olgun kütüphaneleri ve geniş topluluğu.
- `print()` ekrana yazdırır; metinler tırnak içine alınır.
- `#` ile başlayan satırlar çalışmaz, not bırakmak içindir.
- Her bölümde konu anlatımı, ders notları, sınav ve alıştırma var.
