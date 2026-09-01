# Genel Tekrar

Bu bölümde yeni bir şey öğrenmiyorsun. Öğrendiklerinin birbirine nasıl
bağlandığını görüyorsun.

On dört bölüm önce `print("hello")` yazıyordun. Şimdi bir dosyayı okuyup
içindeki veriyi sınıflara dönüştürebiliyor, veritabanına yazabiliyor ve hata
çıktığında ne olduğunu anlayabiliyorsun.

## Öğrendiklerin nasıl bağlanıyor?

Parçaları tek tek öğrendin, ama gerçek bir programda hepsi bir arada
çalışıyor:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Dosya</b><br>veri gelir</span>
    <span class="arrow">→</span>
    <span class="node"><b>Döngü + koşul</b><br>satırlar işlenir</span>
    <span class="arrow">→</span>
    <span class="node"><b>Sözlük / sınıf</b><br>yapıya girer</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Veritabanı</b><br>kalıcı olur</span>
  </div>
  <figcaption>Her ok bir bölüm. Fonksiyonlar bu akışı parçalara böler, hata yakalama bozuk veriyi durdurmaz, tip belirtimleri de her adımın ne beklediğini yazar.</figcaption>
</figure>

Somut bir örnek — bir satır veriyi okuyup işlemek:

```python
def load_scores(path: str) -> dict[str, int]:
    scores: dict[str, int] = {}

    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                name, value = line.split(",")
                scores[name] = int(value)
    except FileNotFoundError:
        return {}

    return scores
```

Bu on satırda **dokuz bölüm** var: değişkenler, operatörler, koşullar,
döngüler, fonksiyonlar, sözlükler, hata yakalama, tip belirtimleri, dosya
işlemleri. Hiçbiri tek başına yeterli değildi; birlikte bir iş yapıyorlar.

## Bölüm bölüm ne öğrendin?

| Bölüm | Anahtar fikir |
|---|---|
| Başlangıç | Python yorumlanır, satır satır çalışır |
| Değişkenler | Değerin bir tipi vardır ve tip davranışı belirler |
| Operatörler | `/` ondalık verir, `//` tam bölme yapar |
| Koşullar | `elif` zinciri ilk tutan koşulda durur |
| Döngüler | `for` bilinen sayıda, `while` koşul sürdükçe |
| Fonksiyonlar | `print` gösterir, `return` verir — ikisi farklı |
| Listeler | Sıralıdır, indeks sıfırdan başlar, değiştirilebilir |
| Sözlükler | Anahtarla erişilir, sıra değil isim önemlidir |
| Modüller | Hazır kodu `import` ile alırsın |
| Hata Yakalama | Yakalayacak bir şey yapamıyorsan yakalama |
| Tip Belirtimleri | Bir nottur, kural değil; kontrol edilmez |
| Dosya İşlemleri | `with` kapatır, `"w"` siler, `encoding` yazılır |
| Nesne Tabanlı | Veri ve davranış birlikteyse sınıf yazılır |
| Veritabanı | `commit` yoksa değişiklik yoktur |

## En sık yapılan sekiz hata

Bu bölümlerde tekrar tekrar karşına çıkan tuzaklar:

1. **`=` ile `==` karışıklığı.** Biri atar, biri sorar.
2. **`return` yerine `print`.** Yazdıran fonksiyon geriye `None` verir.
3. **İndeks sıfırdan başlar.** Üçüncü eleman `[2]`.
4. **`"w"` dosyayı siler.** Ekleme yapacaksan `"a"`.
5. **`strip()` unutmak.** Dosyadan gelen satır `\n` taşır.
6. **`self.` unutmak.** Nesnenin verisi serbest değişken değildir.
7. **`commit` unutmak.** Veritabanı değişikliği kaybolur.
8. **Çıplak `except`.** Beklemediğin hatayı da yutar.

Hepsinin ortak yanı: **çoğu hata vermez**, sessizce yanlış çalışır. Bu yüzden
kodun çalışması doğru olduğu anlamına gelmiyor.

## Ne zaman ne kullanılır?

Yeni başlayanların en çok zorlandığı şey, elindeki araçlardan hangisini
seçeceğine karar vermek.

**Veriyi neyle tutmalı?**

| Durum | Araç |
|---|---|
| Tek bir değer | Değişken |
| Sıralı çok değer | Liste |
| İsimle erişilecek değerler | Sözlük |
| Değişmeyecek sabit grup | Demet |
| Veri **ve** davranış birlikte | Sınıf |
| Program kapanınca kalmalı | Dosya ya da veritabanı |

**Fonksiyon mu sınıf mı?**

Nesnenin hatırlaması gereken bir şey varsa sınıf, yoksa fonksiyon. `self.` ile
yazılmış bir şey yoksa o sınıf olmamalıdır.

**Dosya mı veritabanı mı?**

Veriyi baştan sona okuyorsan dosya yeterli. "Şu koşula uyanları getir",
"şuna göre grupla" diye soruyorsan veritabanı.

## Kodun okunabilir olması

Çalışan kod yeterli değil. Üç ay sonra kendi kodunu açtığında ne yaptığını
anlayabilmen gerekiyor.

- **Adlar ne olduğunu söylesin.** `x` değil `total`, `d` değil `scores`.
- **Fonksiyon tek bir iş yapsın.** Adını koyamıyorsan muhtemelen iki iş
  yapıyordur.
- **Açıklama `neden`i anlatsın.** Kod zaten `ne`yi söylüyor.
- **Tip belirtimleri imzalara.** Fonksiyonu kullanan kişinin gördüğü tek şey
  odur.

## Sırada ne var?

Python Temelleri bitti. Bundan sonrası dilin kendisi değil, onunla yapılan
işler:

- **Veri Bilimi** — NumPy ile hızlı hesap, pandas ile tablolar,
  görselleştirme. Bu bölümdeki dosya okuma ve sözlük bilgisi doğrudan oraya
  bağlanıyor.
- **SQL** — bu bölümde öğrendiğin `SELECT` ve `WHERE` üstüne `JOIN` geliyor.
- **Makine Öğrenmesi** — modelleme. Veri Bilimi olmadan başlanmıyor.
- **API** — başka sistemlerden veri almak. Sözlük ve hata yakalama şart.
- **Docker** — projeyi her makinede aynı çalıştırmak.

Bu bölümün alıştırmaları da buna göre kuruldu: her biri **birden fazla
bölümü** aynı anda kullanıyor. Gerçek kod da böyle yazılıyor.

## Özet

- Öğrendiğin parçalar tek başına değil, birlikte iş yapıyor.
- Hataların çoğu hata vermez; kodun çalışması doğru olduğu anlamına gelmez.
- Aracı seçmek, aracı bilmek kadar önemli: liste mi sözlük mü, fonksiyon mu
  sınıf mı, dosya mı veritabanı mı.
- Okunabilir kod yazmak sonradan eklenen bir süs değil, işin parçası.
- Buradan sonrası dilin kendisi değil, onunla yapılan işler.
