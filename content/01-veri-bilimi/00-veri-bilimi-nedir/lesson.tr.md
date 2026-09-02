# Veri Bilimi Nedir?

Python Temelleri'ni bitirdin. Değişken yazabiliyor, döngü kurabiliyor,
dosya okuyabiliyor, veritabanına sorgu atabiliyorsun. Bu bölümden itibaren
bunları **bir soruya cevap vermek** için kullanacaksın.

Veri bilimi kısaca şu: elinde bir yığın kayıt var, sen ondan bir cümle
çıkarmak istiyorsun.

- 3.000 satırlık satış kaydı → *"Hangi şehirde satış düşüyor?"*
- 50.000 satırlık log dosyası → *"Hata en çok ne zaman çıkıyor?"*
- 800 öğrencinin notu → *"Devamsızlık notu gerçekten etkiliyor mu?"*

Soru cümleyle başlıyor, cevap da cümleyle bitiyor. Arada kalan kısım bu
patikanın konusu.

## Akış

Her veri işi aşağı yukarı aynı beş adımdan geçiyor:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Soru</b><br>ne öğrenmek istiyorum</span>
    <span class="arrow">→</span>
    <span class="node"><b>Veri</b><br>oku, bir araya getir</span>
    <span class="arrow">→</span>
    <span class="node"><b>Temizlik</b><br>eksik, bozuk, tekrar</span>
    <span class="arrow">→</span>
    <span class="node"><b>Analiz</b><br>filtrele, grupla, hesapla</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Cevap</b><br>sayı, grafik, karar</span>
  </div>
  <figcaption>Zamanın büyük kısmı ortadaki iki kutuda geçiyor. Kodun heyecanlı kısmı sonda ama iş oraya gelene kadar bitiyor.</figcaption>
</figure>

Bu adımların hiçbiri sihirli değil. Hepsini şu anda bildiğin Python'la
yapabilirsin — bu bölümde tam olarak onu yapacaksın.

## Veri neye benziyor?

Veri bilimindeki verinin neredeyse tamamı **tablo** şeklinde: satırlar ve
sütunlar.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">satır</span><span class="anat-body">bir kayıt — bir öğrenci, bir satış, bir ölçüm</span></div>
    <div class="anat-row"><span class="anat-label">sütun</span><span class="anat-body">bir özellik — isim, şehir, not, tarih</span></div>
    <div class="anat-row"><span class="anat-label">hücre</span><span class="anat-body">tek bir değer — <code>"Ankara"</code>, <code>82</code></span></div>
  </div>
</figure>

Python'da bu tabloyu tutmanın en doğal yolu **sözlüklerden oluşan bir liste**:

```python
students = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
]
```

Her sözlük bir satır, her anahtar bir sütun. Bir excel dosyasını,
veritabanı sorgusunun sonucunu ya da bir CSV dosyasını Python'a aldığında
karşına genelde tam olarak bu yapı çıkıyor.

## İlk soru: ortalama kaç?

```python
total = 0
for student in students:
    total = total + student["score"]

average = total / len(students)
print(average)
```

```text
82.33333333333333
```

Çalışıyor. Ama dikkat et: **ortalama almak için üç satır yazdın.** Basit bir
soru için fazla.

## İkinci soru: Ankara'da ortalama kaç?

```python
ankara_scores = []
for student in students:
    if student["city"] == "Ankara":
        ankara_scores.append(student["score"])

average = sum(ankara_scores) / len(ankara_scores)
print(average)
```

```text
86.5
```

Yine çalışıyor. Ama bir soru daha soruldu ve kod bir kat daha uzadı.

## Üçüncü soru: her şehirde ortalama kaç?

```python
totals = {}
counts = {}

for student in students:
    city = student["city"]
    totals[city] = totals.get(city, 0) + student["score"]
    counts[city] = counts.get(city, 0) + 1

averages = {}
for city in totals:
    averages[city] = totals[city] / counts[city]

print(averages)
```

```text
{'Ankara': 86.5, 'Izmir': 74.0}
```

On satır. Ve bu, üç satırlık bir veri için.

## İşte sorun burada

Yazdığın kod yanlış değil. Sorun şu: **soru büyüdükçe kod da büyüyor** ve
büyüyen kodda hata yapmak kolay. `counts` sözlüğünü güncellemeyi
unutursan sonuç sessizce yanlış çıkıyor — program çökmüyor, sana yanlış bir
sayı veriyor.

Bir de hız var. Üç satırda fark etmiyor ama **üç milyon satırda** Python
döngüsü dakikalar sürüyor.

Bu iki sorun için iki kütüphane var ve bu patikanın büyük kısmı onları
öğrenmek:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>NumPy</h4>
      <p>Sayı dizileriyle hesap. Döngü yazmadan bütün diziyle tek seferde işlem yapıyor ve bunu C hızında yapıyor.</p>
    </div>
    <div class="versus-side">
      <h4>pandas</h4>
      <p>Tablolarla çalışma. Okuma, filtreleme, gruplama, birleştirme — hepsi hazır. NumPy'ın üstüne kurulu.</p>
    </div>
  </div>
</figure>

Yukarıdaki on satırlık şehir ortalaması, pandas'ta şu:

```python
data.groupby("city")["score"].mean()
```

Tek satır. Bu bölümün sonunda bu satırı henüz yazamayacaksın — ama onun
neyin yerine geçtiğini tam olarak bileceksin. **Kütüphaneyi önce elle
yaptığın için anlıyorsun.**

## Kütüphaneler nereden geliyor?

`sqlite3` Python'un içinde geliyordu; NumPy ve pandas gelmiyor. Onlar ayrı
kurulan paketler:

```text
pip install numpy pandas
```

Odyssey bunu senin için hallediyor — alıştırmaların çalıştığı ortamda bu
paketler zaten kurulu. Kendi bilgisayarında bir proje yaparken ise
`Modüller` bölümünde anlatılan sanal ortam yöntemini kullanacaksın.

## Bu bölümde ne yapacaksın

Beş alıştırmanın hepsi **kütüphanesiz**. Ortalama alacaksın, satır
filtreleyeceksin, sütun çıkaracaksın, gruplayacaksın ve küçük bir özet
raporu yazdıracaksın — hepsi düz Python'la.

Amaç şu: sonraki bölümde `mean()` yazdığında bunun arkasında ne olduğunu
biliyor olman. Kütüphane, işi bilmeyene kolaylık sağlamıyor; işi bilenin
zamanını kazandırıyor.

## Özet

- Veri bilimi bir **soruyla** başlar, veriyle biter — kodla değil.
- Akış hep aynı: soru → veri → temizlik → analiz → cevap.
- Veri neredeyse hep **tablo**: satır = kayıt, sütun = özellik.
- Python'da tablo genelde **sözlüklerden oluşan bir liste**.
- Düz Python'la her şey yapılabiliyor ama kod hızla uzuyor ve büyük veride
  yavaş kalıyor.
- **NumPy** sayı dizileri için, **pandas** tablolar için. İkisi de dışarıdan
  kurulan paketler.
